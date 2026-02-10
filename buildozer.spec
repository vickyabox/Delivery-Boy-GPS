[app]
# App ka naam aur version
title = My Delivery Spots
package.name = deliveryspots
package.domain = org.deliveryboy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0

# Zaroori requirements (plyer add kiya hai GPS ke liye)
requirements = python3,kivy,kivymd,android,plyer,openssl

orientation = portrait
fullscreen = 0

# Android Permissions (GPS aur Internet ke liye bahut zaroori)
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
