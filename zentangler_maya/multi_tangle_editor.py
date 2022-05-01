import pymel.core as pm
from zentangler_maya.tangle_editor import TangleEditor
from zentangler.multi_tangle import MultiTangle
class MultiTangleEditor:

    def __init__(self, container_ui, tangles: list, name="multi_tangle"):
        self.container_ui = container_ui
        self.multi_tangle = MultiTangle(tangles)
        self.tangle_editors = []
        with self.container_ui:
            form = pm.formLayout()
            tabs = pm.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
            with tabs:

                child1 = pm.rowColumnLayout(numberOfColumns=1)
                self.tangle_editors.append(TangleEditor(child1, tangles[0]))


                child2 = pm.rowColumnLayout(numberOfColumns=1)
                self.tangle_editors.append(TangleEditor(child2, tangles[0]))

            pm.tabLayout(tabs, edit=True, tabLabel=((child1, 'One')))
            pm.tabLayout(tabs, edit=True, tabLabel=((child2, 'Two')))


    def get_img_folder(self):
        return TangleEditor.get_img_folder_from_name(self.name)

    def get_thumbnail_filename(self):
        return self.get_img_folder() + "/tangle_thumbnail.png"

    def get_png_filename(self):
        return self.get_img_folder() + "/tangle.png"

    def get_svg_filename(self):
        return self.get_img_folder() + "/tangle.svg"


