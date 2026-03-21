function showFileName(input) {
    const name = input.files[0] ? input.files[0].name : "файл не выбран";
    document.getElementById("file-name").textContent = name;
}