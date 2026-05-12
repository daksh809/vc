[app]

title = EMI Calculator
package.name = emicalculator
package.domain = org.test

source.dir = .
source.include_exts = py,kv,png,jpg,ttf

version = 1.0

requirements = python3,kivy==2.2.1,kivymd==1.2.0

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 21

android.accept_sdk_license = True

p4a.branch = master

[buildozer]
log_level = 2
