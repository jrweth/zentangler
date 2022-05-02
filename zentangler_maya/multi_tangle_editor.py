import pymel.core as pm
from zentangler_maya.tangle_editor import TangleEditor
from zentangler.multi_tangle import MultiTangle
class MultiTangleEditor:

    def __init__(self, container_ui, multi_tangle: MultiTangle):
        self.container_ui = container_ui
        self.multi_tangle = multi_tangle
        self.tangle_editors = []
        multi_tangle.create_all()
        with self.container_ui:
            form = pm.formLayout()
            tabs = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
            with tabs:
                for i in range(len(multi_tangle.tangles)):
                    tangle_editor = pm.rowColumnLayout(numberOfColumns=1)
                    self.tangle_editors.append(TangleEditor(tangle_editor, multi_tangle.tangles[i], self))
                    pm.tabLayout(tabs, edit=True, tabLabel=((tangle_editor, "shape " + str(i+1))))

    def get_img_folder(self):
        return TangleEditor.get_img_folder_from_name(self.multi_tangle.tangle_name)

    def get_thumbnail_filename(self):
        return self.get_img_folder() + "/tangle_thumbnail.png"

    def get_png_filename(self):
        return self.get_img_folder() + "/tangle.png"

    def get_svg_filename(self):
        return self.get_img_folder() + "/tangle.svg"

    def refresh(self):
        self.multi_tangle.create_combined_png(self.get_png_filename())

