"""Keep Android user files outside the replaceable cooked Player install."""

import re
from pathlib import Path


ACTIVITY = (
    Path(__file__).resolve().parents[1]
    / "package/editor/infernux_android/templates/host/app/src/main/java/com/infernux/bootstrap/InfernuxActivity.java"
)


def test_player_upgrade_cannot_replace_persistent_files():
    source = ACTIVITY.read_text(encoding="utf-8")
    roots = dict(
        re.findall(
            r'private static final String (PLAYER_ASSET_ROOT|USER_DATA_ROOT) = "([^"]+)";',
            source,
        )
    )

    assert roots.keys() == {"PLAYER_ASSET_ROOT", "USER_DATA_ROOT"}
    assert all("/" not in root and "\\" not in root for root in roots.values())
    assert roots["PLAYER_ASSET_ROOT"] != roots["USER_DATA_ROOT"]
    assert "File installedRoot = new File(getFilesDir(), assetRoot);" in source
    assert "deleteRecursively(installedRoot);" in source
    assert "File persistentData = new File(getFilesDir(), USER_DATA_ROOT);" in source
    assert 'new File(getFilesDir(), "player").getAbsolutePath()' not in source


def test_player_loose_files_use_the_separate_persistent_root():
    source = ACTIVITY.read_text(encoding="utf-8")
    startup = source.split("protected void onCreate(Bundle savedInstanceState)", 1)[1].split(
        "super.onCreate(savedInstanceState);", 1
    )[0]

    assert 'File looseFiles = new File(persistentData, "loose");' in startup
    assert "!looseFiles.isDirectory() && !looseFiles.mkdirs()" in startup
    assert re.search(
        r'Os\.setenv\(\s*"_INFERNUX_PLAYER_PERSISTENT_DATA_ROOT",'
        r'\s*persistentData\.getAbsolutePath\(\)',
        startup,
    )
    assert re.search(
        r'Os\.setenv\(\s*"_INFERNUX_PLAYER_INSTALL_ROOT",'
        r'\s*looseFiles\.getAbsolutePath\(\)',
        startup,
    )
    assert startup.index("looseFiles.mkdirs()") < startup.index(
        '"_INFERNUX_PLAYER_INSTALL_ROOT"'
    )
