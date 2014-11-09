import sublime
import sublime_plugin

import re
import os
from os import path

try:
  from QuickSearchEnhanced import quick_search

  from FolderFiles.folder_files import(FolderFiles, open_file_or_folder_by_panel,
    open_folder_by_panel)
except ImportError:
  sublime.error_message("Dependency import failed; please read readme for " +
   "FileDialog plugin for installation instructions; to disable this " +
   "message remove this plugin")

class PromptOpenFileEnhanced(sublime_plugin.TextCommand):
  def run(self, edit, path = None):
    if path == None and self.view.file_name() != None:
      path = os.path.dirname(self.view.file_name())

    if path == None:
      path = get_preferred_view_path(self.view)
      path = path != None and os.path.dirname(path) or None

    if path == None:
      folders = sublime.active_window().folders()
      if len(folders) > 0:
        path = folders[0]

    if path == None:
      return

    FolderFiles(path, status = '📂').show()

views_paths = {}

def set_preferred_view_path(view, path):
  views_paths[view.id()] = path

def get_preferred_view_path(view):
  if view.id() not in views_paths:
    return None

  return views_paths[view.id()]

class Save():
  def __init__(self, view, status = '', remove = False):
    self.view = view
    self.remove = remove
    path = self._get_view_directory()

    options = {'text': self._get_view_name()}
    caller = [['save', self]]
    self.folder = FolderFiles(path, None, False, status, options, caller,
      self._on_create)

  def _on_create(self, panel):
    text = panel.get_current_text()
    if text.strip() == '':
      return

    match = re.search(r'\.[^\.]+$', text)
    if match == None:
      return None

    view = panel.get_panel()
    view.sel().clear()
    view.sel().add(sublime.Region(0, match.start(0)))

  def _get_view_name(self):
    if self.view.file_name() != None:
      return path.basename(self.view.file_name())

    file_name = get_preferred_view_path(self.view) or ''
    file_name = path.basename(file_name)

    region = sublime.Region(0, min(self.view.size(), 1024 * 50))
    contents = self.view.substr(region)
    class_name = re.search(r'\nclass.*?(\w+)[\s\(:](?!:)', contents)
    if class_name != None:
      _, extension = path.splitext(file_name)
      file_name = class_name.group(1) + extension

    return file_name

  def _get_view_directory(self):
    if self.view.file_name() != None:
      return os.path.dirname(self.view.file_name())
    elif get_preferred_view_path(self.view) != None:
      return path.dirname(get_preferred_view_path(self.view))
    else:
      return sublime.active_window().folders()[0]

  def get_view(self):
    return self.view

  def is_remove(self):
    return self.remove

  def show(self):
    self.folder.show()

  def save(self, file_name):
    try:
      path = self.folder.get_current_path() + '/' + file_name
      if os.path.isdir(path):
        sublime.error_dialog('File "' +path + '" is directory; can not save')
        return None

      overwrite = not os.path.isfile(path) or(sublime.ok_cancel_dialog('File "' +
        path + '" exists; ' +'do you want to overwrite it?', 'OVERWRITE'))

      if not overwrite:
        return None

      file = open(path, 'w')
      file.write(self.view.substr(sublime.Region(0, self.view.size())))
      file.close()
    except Exception as error:
      sublime.error_message('Error while saving file: {0}'.format(error))
      return None

    return path

class PromptSaveAsEnhanced(sublime_plugin.TextCommand):
  def run(self, edit):
    Save(self.view, '💾').show()

class PromptRenameFile(sublime_plugin.TextCommand):
  def run(self, edit):
    Save(self.view, '♻', True).show()

class SaveEnhanced(sublime_plugin.TextCommand):
  def run(self, edit):
    if self.view.file_name() != None:
      sublime.set_timeout(self._save, 10)
    else:
      self.view.run_command('prompt_save_as_enhanced')

  def _save(self):
    self.view.run_command('save')

class SaveEnhancedComplete(sublime_plugin.TextCommand):
  def run(self, edit):
    panel = quick_search.panels.get_current()
    save = panel.get_caller('save')
    if save == None:
      return

    panel.hide()

    file_name = save.save(panel.get_current_text())
    if file_name == None:
      panel.show()
      return

    panel.close(None, False)

    window = sublime.active_window()
    view = save.get_view()

    old_file_name = view.file_name()

    remove = (old_file_name != None and os.path.isfile(old_file_name) and
      save.is_remove())
    if remove:
      os.remove(old_file_name)

    window.focus_view(view)
    view.set_scratch(True)
    window.run_command('close_file')
    window.open_file(file_name)

class ViewPathSaver(sublime_plugin.EventListener):
  def __init__(self):
    self.save_most_recent_path = None

  def on_new(self, view):
    set_preferred_view_path(view, self.save_most_recent_path)

  def on_activated(self, view):
    if view.file_name() == None:
      return

    self.save_most_recent_path = view.file_name()