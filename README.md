# cleanMaterials

cleanMaterials is a Blender Python script that previews and removes materials that are no longer used by the current file.

The script only targets local materials with zero users. Materials protected by Fake User or linked from an external library are preserved.

## Compatibility

Tested and confirmed working with Blender 3.6 and Blender 5.2.

## Requirements

- Blender with Python scripting support
- A `.blend` file containing materials

## Usage

1. Download `cleanMaterials.py`.
2. Open Blender and switch to the **Scripting** workspace.
3. Open `cleanMaterials.py` in the Text Editor.
4. Click **Run Script**.
5. Review the unused materials shown in the preview dialog.
6. Click **Delete Materials** to confirm.

The operation can be undone with **Ctrl+Z**. If no unused materials are found, the script leaves the file unchanged.

## Notes

- Materials with Fake User enabled are preserved.
- Materials linked from external libraries are preserved.
- The preview lists up to 12 material names and reports how many additional materials were found.
- Removal results and any failures are written to Blender's console.
- Save a backup of important `.blend` files before running cleanup scripts.

## Author

SZ

- [Bilibili](https://space.bilibili.com/12379590)

## License

Released under the [MIT License](LICENSE).
