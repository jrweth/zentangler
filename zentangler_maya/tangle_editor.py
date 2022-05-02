from zentangler.tangle import Tangle
from zentangler_maya.rule_editor import RuleEditor
import pymel.core as pm
import os

class TangleEditor:

    def __init__(self, parent_layout, tangle: Tangle, parent_multi_tangle_editor=None):
        # the parent layout to place the tangle editor in
        self.parent_layout = parent_layout

        # the tangle
        self.tangle = tangle

        # message to display in the tangle
        self.message = ""

        # ui element to display the message
        self.message_ui = None

        # image ui element that holds the thumbnail
        self.tangle_thumbnail = None

        # container to hold the rules in
        self.rules_container = None

        self.parent_multi_tangle_editor = parent_multi_tangle_editor

        # create our container
        with self.parent_layout:
            self.container_layout = pm.columnLayout(adjustableColumn=False, rowSpacing=10)
        self.create_ui_elements()

    def refresh_tangle(self):
        self.set_message("refreshing tangle")
        self.tangle.re_expand()
        self.generate_thumbnail()
        self.generate_png()
        if self.parent_multi_tangle_editor is not None:
            self.parent_multi_tangle_editor.refresh()
        self.set_message("")
        pm.refresh()

    def create_ui_elements(self):
        with self.container_layout:
            self.tangle_thumbnail = pm.image(
                image=self.get_thumbnail_filename(),
                backgroundColor=[0.5, 0.5, 0.5],
                width=256
            )
            pm.button("Refresh Tangle", command=pm.Callback(TangleEditor.refresh_tangle, self))
            self.message_ui = pm.text("Generating Tangle")
            with pm.scrollLayout(height=400):
                self.rules_container = pm.columnLayout(adjustableColumn=False, height=4000)
            self.add_grammar_rule_widgets()
        self.generate_thumbnail()

    def add_grammar_rule_widgets(self):
        for rule_index in range(len(self.tangle.grammar.rules)):
            RuleEditor(self, rule_index)

    def get_img_folder_from_name(name: str):
        zentangler_path = pm.workspace.getPath() + "/zentangler"
        if not os.path.isdir(zentangler_path):
            os.mkdir(zentangler_path)
        tangle_path = zentangler_path + "/" + name
        if not os.path.isdir(tangle_path):
            os.mkdir(tangle_path)
        return tangle_path

    def get_img_folder(self):
        return TangleEditor.get_img_folder_from_name(self.tangle.name)

    def set_message(self, message):
        self.message = message
        self.message_ui.setLabel(self.message)

    def get_thumbnail_filename(self):
        return self.get_img_folder() + "/tangle_thumbnail.png"

    def get_png_filename(self):
        return self.get_img_folder() + "/tangle.png"

    def generate_thumbnail(self):
        # if we haven't run the tangle yet then do so
        if len(self.tangle.history) <= 1:
            self.message = "Creating Tangle"
            self.tangle.create()
            self.message = ""
        self.tangle.create_last_expansion_png(self.get_thumbnail_filename(), 256)
        self.tangle_thumbnail.setImage(self.get_thumbnail_filename())

    def generate_png(self):
        # if we haven't run the tangle yet then do so
        if len(self.tangle.history) <= 1:
            self.message = "Creating Tangle"
            self.tangle.create()
            self.message = ""
        self.tangle.create_last_expansion_png(self.get_png_filename(), 2048)


