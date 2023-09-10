#!/usr/bin/env python3

from glob import glob
from os.path import basename, splitext
files = glob("/mnt/NZReefs/**/*.tif", recursive=True)

print("""MAP
    PROJECTION
        "init=epsg:3857" # Output projection
    END""")

for filepath in files:
    name = splitext(basename(filepath))[0]
    print(f"""
    LAYER
        NAME "{name}"
        DATA "{filepath}"
        TYPE RASTER
        PROJECTION
            "init=epsg:4326"
        END
        STATUS ON
    END""")
print("""
    WEB
        METADATA
            "wms_title" "NZReefs imagery"
            "wms_enable_request"  "*"
        END
    END
END
""")
