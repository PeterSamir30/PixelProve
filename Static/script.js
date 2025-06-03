document.addEventListener('DOMContentLoaded', function () {
    const aiImageInput = document.getElementById('aiImage');
    const aiFileNameSpan = document.getElementById('aiFileName');
    const deepfakeFaceInput = document.getElementById('deepfakeFace');
    const deepfakeFileNameSpan = document.getElementById('deepfakeFileName');

    if (aiImageInput) {
        aiImageInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                aiFileNameSpan.textContent = this.files[0].name;
            } else {
                aiFileNameSpan.textContent = 'No file chosen';
            }
        });
    }

    if (deepfakeFaceInput) {
        deepfakeFaceInput.addEventListener('change', function () {
            if (this.files && this.files[0]) {
                deepfakeFileNameSpan.textContent = this.files[0].name;
            } else {
                deepfakeFileNameSpan.textContent = 'No file chosen';
            }
        });
    }


    console.log("JS Loaded");
});