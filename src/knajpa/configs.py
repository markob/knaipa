"""This file contains Settings Manager and is an unique access point to all settings."""

class __SettingsManager(dict):
  _data = {}

SettingsManager = __SettingsManager()
