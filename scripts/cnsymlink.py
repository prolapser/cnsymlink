import modules.scripts as scripts
import gradio as gr
import os
import subprocess

sdroot = "/".join(os.path.realpath(__file__).split("extensions")[0].split("/")[:-1])

sdmodels = os.path.join(sdroot, "models/ControlNet")
controlnet_path = os.path.join(sdroot, "extensions/rectal_control/")
controlnet_temp = os.path.join(controlnet_path, "tmp")
controlnet_models_path = os.path.join(controlnet_path, "models")
controlnet_annotators_path = os.path.join(controlnet_path, "annotator")


# создание симлинков из общей папки в среду выполнения gdshare_linker("ControlNet/models", controlnet_path)
def gdshare_linker(gdpath, dest_path) -> str:
    gdrive_folder = "/content/drive/MyDrive/colab_files/"
    gdpath = f"{gdrive_folder}{gdpath}"
    target = os.path.join(dest_path, gdpath.split('/')[-2] if gdpath.endswith('/') else gdpath.split('/')[-1])
    os.makedirs(dest_path, exist_ok=True)
    os.makedirs(controlnet_temp, exist_ok=True)

    def linking():
        for root, dirs, files in os.walk(gdpath):
            for file in files:
                file_path = os.path.join(root, file)
                dest_file_path = os.path.join(dest_path, file)
                if not os.path.exists(dest_file_path):
                    subprocess.run(['ln', '-s', file_path, dest_file_path], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                    if not os.path.exists(dest_file_path):
                        os.symlink(file_path, dest_file_path)

    if os.path.exists(gdpath):
        try:
            linking()
            return "файлы успешно добавлены! теперь нужно нажать кнопку 🔄 обновления в дополнении контролнета. ВНИМАНИЕ: прогресс обновления файлов в селекторе моделей у контролнета никак не отображается и но это занимает ЗНАЧИТЕЛЬНОЕ время!!!"
        except FileExistsError:
            try:
                subprocess.run(['rm', '-rf', target], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
                linking()
                return "файлы были заменены, т.к. присутствовали с тем же именем. теперь нужно нажать кнопку 🔄 обновления в дополениии контролнета. ВНИМАНИЕ: прогресс обновления файлов в селекторе моделей у контролнета никак не отображается и но это занимает ЗНАЧИТЕЛЬНОЕ время!!!"
            except Exception as e:
                return f"ошибка: {e}"
        except OSError:
            return "создать симлинк не удалось!"
    else:
        if not os.path.exists(gdpath):
            return "на твоем гуглодиске не найдена общая папка с моделями контролнет"
        else:
            return "хз"


class ExtensionTemplateScript(scripts.Script):
    def title(self):
        return "добавить модели ControlNet"

    def show(self, is_img2img):
        return scripts.AlwaysVisible

    def ui(self, is_img2img):
        with gr.Accordion('модели ControlNet', elem_id="controlnet_models_gdrive", open=False):
            def cn_sd():
                gdshare_linker("ControlNet/bin/sd", sdmodels)
                return gdshare_linker("ControlNet/models", controlnet_models_path)

            def cn_sdxl():
                gdshare_linker("ControlNet/bin/sdxl", sdmodels)
                return gdshare_linker("ControlNet/models_xl", controlnet_models_path)

            cnsymlinker_results = gr.Textbox(value="нажми на кнопку ⬇️ чтобы добавить соответствующие модели", label="", lines=10, elem_id="cnsymlinker_results")
            cn_sd_button = gr.Button("модели SD", elem_id="cn_sd_symlinker_button")
            cn_sdxl_button = gr.Button("модели SDXL", elem_id="cn_sdxl_symlinker_button")
            cn_sd_button.click(fn=cn_sd, outputs=cnsymlinker_results)
            cn_sdxl_button.click(fn=cn_sdxl, outputs=cnsymlinker_results)

        return [cnsymlinker_results, cn_sd_button, cn_sdxl_button]
