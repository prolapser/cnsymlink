function moveSymlinkerButtons() {
    setTimeout(function () {
        var txt2img_script_container = document.getElementById("txt2img_script_container");
        var cn_symlink_buttons_txt2img = document.createElement("div");
        cn_symlink_buttons_txt2img.id = "cn_symlinker_buttons";
        var sd_cn_button_txt2img = txt2img_script_container.querySelector("#cn_sd_symlinker_button");
        var sdxl_cn_button_txt2img = txt2img_script_container.querySelector("#cn_sdxl_symlinker_button");
        var controlnet_ext_tabs_txt2img = txt2img_script_container.querySelector("#txt2img_controlnet_tabs");
        sd_cn_button_txt2img.parentNode.insertBefore(cn_symlink_buttons_txt2img, sd_cn_button_txt2img);
        cn_symlink_buttons_txt2img.appendChild(sd_cn_button_txt2img);
        cn_symlink_buttons_txt2img.appendChild(sdxl_cn_button_txt2img);
        var cn_symlink_container_txt2img = cn_symlink_buttons_txt2img.parentNode;
        cn_symlink_container_txt2img.id = "cn_symlynk_container";
        controlnet_ext_tabs_txt2img.insertBefore(cn_symlink_container_txt2img, controlnet_ext_tabs_txt2img.firstChild);
    
    }, 1000);
    
    setTimeout(function () {
        var img2img_script_container = document.getElementById("img2img_script_container");
        var cn_symlink_buttons_img2img = document.createElement("div");
        cn_symlink_buttons_img2img.id = "cn_symlinker_buttons";
        var sd_cn_button_img2img = img2img_script_container.querySelector("#cn_sd_symlinker_button");
        var sdxl_cn_button_img2img = img2img_script_container.querySelector("#cn_sdxl_symlinker_button");
        var controlnet_ext_tabs_img2img = img2img_script_container.querySelector("#img2img_controlnet_tabs");
        sd_cn_button_img2img.parentNode.insertBefore(cn_symlink_buttons_img2img, sd_cn_button_img2img);
        cn_symlink_buttons_img2img.appendChild(sd_cn_button_img2img);
        cn_symlink_buttons_img2img.appendChild(sdxl_cn_button_img2img);
        var cn_symlink_container_img2img = cn_symlink_buttons_img2img.parentNode;
        cn_symlink_container_img2img.id = "cn_symlynk_container";
        controlnet_ext_tabs_img2img.insertBefore(cn_symlink_container_img2img, controlnet_ext_tabs_img2img.firstChild);
    }, 1500);
}


function onElementsLoaded(elementsToObserve, callback) {
    const elementsStatus = elementsToObserve.reduce((status, selector) => {
        status[selector] = false;
        return status;
    }, {});

    function checkElementsStatus() {
        if (Object.values(elementsStatus).every(status => status)) {
            observer.disconnect();
            callback();
        }
    }

    const observer = new MutationObserver(mutations => {
        mutations.forEach(mutation => {
            if (mutation.addedNodes.length) {
                elementsToObserve.forEach(selector => {
                    if (document.querySelector(selector)) {
                        elementsStatus[selector] = true;
                    }
                });
                checkElementsStatus();
            }
        });
    });

    observer.observe(document.body, {
        childList: true,
        subtree: true
    });

    elementsToObserve.forEach(selector => {
        if (document.querySelector(selector)) {
            elementsStatus[selector] = true;
        }
    });
    checkElementsStatus();
}


const elementsToObserve = [
    '#txt2img_controlnet',
    '#img2img_controlnet',
    '#controlnet_models_gdrive',
    '#cn_sd_symlinker_button',
    '#cn_sdxl_symlinker_button',
    '#txt2img_script_container',
    '#img2img_script_container'
];

document.addEventListener('DOMContentLoaded', function () {
    onUiLoaded(function () {
        onElementsLoaded(elementsToObserve, () => {
            moveSymlinkerButtons();
        });
    });
});
