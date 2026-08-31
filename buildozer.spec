[app]

# Title
title = Rubika Bot

# Package name
package.name = rubikabot
package.domain = com.rubikabot

# Source
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Version
version = 1.0.0

# Requirements - NO rubpy, just basic libs
requirements = python3,kivy

# Android settings
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# Orientation
orientation = portrait

# Fullscreen
fullscreen = 0

# Log level
log_level = 2

# P4a recipes
p4a.branch = develop
