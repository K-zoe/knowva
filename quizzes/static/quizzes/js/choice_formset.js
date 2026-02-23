document.addEventListener("DOMContentLoaded", () => {
    const formset = document.getElementById("choice-formset");
    const addBtn = document.getElementById("add-choice");
    const form = document.querySelector(".problem-form");

    const prefix = formset.dataset.prefix;
    const totalFormsInput = document.querySelector(
        `input[name="${prefix}-TOTAL_FORMS"]`
    );

    function updateChoiceNumbers() {
        const forms = document.querySelectorAll(".choice-form");
        forms.forEach((form, index) => {
            const number = form.querySelector(".choice-number");
            number.textContent = `選択肢 ${index + 1}`;
        });
    }

    function hasAtLeastOneCorrect() {
        return [...document.querySelectorAll(
            `input[name$="-is_correct"]`
        )].some(cb => cb.checked);
    }

    addBtn.addEventListener("click", () => {
        const forms = document.querySelectorAll(".choice-form");
        const newIndex = forms.length;

        const newForm = forms[0].cloneNode(true);

        newForm.querySelectorAll("input, textarea").forEach(input => {
            if (input.name) {
                input.name = input.name.replace(/-\d+-/, `-${newIndex}-`);
                input.id = input.id.replace(/-\d+-/, `-${newIndex}-`);
            }

            if (input.type === "checkbox") {
                input.checked = false;
            } else {
                input.value = "";
            }
        });

        formset.appendChild(newForm);
        totalFormsInput.value = newIndex + 1;
        updateChoiceNumbers();
    });

    formset.addEventListener("click", (e) => {
        if (!e.target.classList.contains("btn-delete-choice")) return;

        const forms = document.querySelectorAll(".choice-form");
        if (forms.length <= 2) {
            alert("選択肢は最低2つ必要です。");
            return;
        }

        e.target.closest(".choice-form").remove();
        totalFormsInput.value = document.querySelectorAll(".choice-form").length;
        updateChoiceNumbers();
    });

    // ✅ 正解が最低1つ必須チェック
    form.addEventListener("submit", (e) => {
        if (!hasAtLeastOneCorrect()) {
            e.preventDefault();
            alert("正解の選択肢を最低1つ選んでください。");
        }
    });
});


document.addEventListener('DOMContentLoaded', () => {

    const choiceForms = document.querySelectorAll('.choice-form');

    choiceForms.forEach(form => {
        const deleteCheckbox = form.querySelector('input[type="checkbox"][name$="-DELETE"]');
        const correctCheckbox = form.querySelector('input[type="checkbox"][name$="-is_correct"]');

        if (!deleteCheckbox || !correctCheckbox) return;

        // 削除にチェック → 正解を外す
        deleteCheckbox.addEventListener('change', () => {
            if (deleteCheckbox.checked) {
                correctCheckbox.checked = false;
                correctCheckbox.disabled = true; // ← 任意（UX向上）
            } else {
                correctCheckbox.disabled = false;
            }
        });
    });

});