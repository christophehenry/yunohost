import dbus

from moulinette.utils.log import getActionLogger

logger = getActionLogger("yunohost.storage")


UDISK_DRIVE_PATH = "/org/freedesktop/UDisks2/drives/"
UDISK_DRIVE_IFC = "org.freedesktop.UDisks2.Drive"


def infos():
    result = {}

    bus = dbus.SystemBus()
    manager = dbus.Interface(
        bus.get_object("org.freedesktop.UDisks2", "/org/freedesktop/UDisks2"),
        "org.freedesktop.DBus.ObjectManager",
    )

    for name, dev in manager.GetManagedObjects().items():
        if not name.startswith(UDISK_DRIVE_PATH):
            continue

        drive = dev[UDISK_DRIVE_IFC]
        name = name.removeprefix(UDISK_DRIVE_PATH)
        rotation_rate = drive["RotationRate"]
        result[name] = {
            "name": name,
            "model": drive["Model"],
            "serial": drive["Serial"],
            "size": drive["Size"],
            "type": "HDD" if rotation_rate != 0 else "SSD",
            "rpm": rotation_rate if rotation_rate != 0 else None,
        }

    return result
