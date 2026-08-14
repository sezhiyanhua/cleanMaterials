"""cleanMaterials - Unused material cleaner for Blender 3.6 and later.

Author: SZ
bilibili: https://space.bilibili.com/12379590
"""

import bpy


MAX_PREVIEW_ITEMS = 12


def find_unused_materials() -> list[bpy.types.Material]:
    return [
        material
        for material in bpy.data.materials
        if not material.use_fake_user
        and material.users == 0
        and material.library is None
    ]


def remove_materials(
    materials: list[bpy.types.Material],
) -> tuple[list[str], list[tuple[str, str]]]:
    removed_names: list[str] = []
    failures: list[tuple[str, str]] = []

    for material in materials:
        name = material.name
        try:
            bpy.data.materials.remove(material, do_unlink=False)
            removed_names.append(name)
        except (RuntimeError, ReferenceError) as error:
            failures.append((name, str(error)))

    return removed_names, failures


def show_result_popup(removed_count: int, failed_count: int) -> None:
    if bpy.app.background:
        return

    if failed_count:
        title = "cleanMateria - Completed with Warnings"
        icon = "ERROR"
        message = f"Removed {removed_count}; failed to remove {failed_count}."
    elif removed_count:
        title = "cleanMateria - Success"
        icon = "CHECKMARK"
        message = f"Success! Removed {removed_count} material(s)."
    else:
        title = "cleanMateria"
        icon = "INFO"
        message = "Nothing to clean. No unused materials found."

    def draw(self, _context):
        self.layout.label(text=message, icon=icon)

    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)


class CLEANMATERIA_OT_clean(bpy.types.Operator):
    bl_idname = "cleanmateria.clean"
    bl_label = "Clean Unused Materials"
    bl_description = "Preview and remove truly unused materials"
    bl_options = {"REGISTER", "UNDO"}

    def invoke(self, context, _event):
        candidates = find_unused_materials()
        if not candidates:
            self.report({"INFO"}, "Nothing to clean: no unused materials found")
            show_result_popup(0, 0)
            return {"CANCELLED"}

        try:
            return context.window_manager.invoke_props_dialog(
                self,
                width=460,
                title="Preview Unused Materials",
                confirm_text="Delete Materials",
            )
        except TypeError:
            return context.window_manager.invoke_props_dialog(self, width=460)

    def draw(self, _context):
        layout = self.layout
        candidates = find_unused_materials()

        layout.label(
            text=f"{len(candidates)} unused material(s) will be deleted.",
            icon="INFO",
        )
        layout.label(text="This operation can be undone with Ctrl+Z.")
        layout.separator()

        column = layout.column(align=True)
        for material in candidates[:MAX_PREVIEW_ITEMS]:
            column.label(text=material.name, icon="MATERIAL")

        remaining = len(candidates) - MAX_PREVIEW_ITEMS
        if remaining > 0:
            column.label(text=f"...and {remaining} more")

    def execute(self, _context):
        candidates = find_unused_materials()
        removed_names, failures = remove_materials(candidates)

        print(
            f"[cleanMateria] Removed {len(removed_names)} material(s); "
            f"failed: {len(failures)}."
        )
        for name in removed_names:
            print(f"  [removed] {name}")
        for name, reason in failures:
            print(f"  [failed] {name}: {reason}")

        show_result_popup(len(removed_names), len(failures))

        if failures:
            self.report(
                {"WARNING"},
                f"Removed {len(removed_names)} material(s); "
                f"{len(failures)} failed. See the console for details.",
            )
        elif removed_names:
            self.report(
                {"INFO"},
                f"Success! Removed {len(removed_names)} material(s).",
            )
        else:
            self.report({"INFO"}, "Nothing to clean")

        return {"FINISHED"}


def register() -> None:
    existing_class = getattr(bpy.types, CLEANMATERIA_OT_clean.__name__, None)
    if existing_class is not None:
        bpy.utils.unregister_class(existing_class)
    bpy.utils.register_class(CLEANMATERIA_OT_clean)


def main() -> None:
    register()
    if bpy.app.background:
        bpy.ops.cleanmateria.clean("EXEC_DEFAULT")
    else:
        bpy.ops.cleanmateria.clean("INVOKE_DEFAULT")


if __name__ == "__main__":
    main()
