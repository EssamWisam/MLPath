document.addEventListener('DOMContentLoaded', async () => {
    const modelsListItems = document.querySelectorAll('.sidebar .parent-list li.model-name');
    const questsListItems = document.querySelectorAll('.sidebar .child-list li.quest-name');
    const refreshButton = document.querySelector('#refresh-button');
    const columnsButton = document.querySelector('#columns-button');
    const searchForm = document.querySelector('#search-form');

    if (!localStorage.getItem('activeModelIndex') || !localStorage.getItem('activeQuestIndex')) {
        localStorage.setItem('activeModelIndex', 0);
        localStorage.setItem('activeQuestIndex', 0);
    }

    loadResults();

    questsListItems.forEach((quest, index) => {
        quest.addEventListener('click', async () => {
            const modelName = quest.dataset.modelName;
            const modelIndex = [...modelsListItems].findIndex(model => model.textContent === modelName);
            localStorage.setItem('activeModelIndex', modelIndex);
            localStorage.setItem('activeQuestIndex', index);
            questsListItems.forEach(quest => quest.classList.remove('active'));
            quest.classList.add('active');
            loadResults();
        });
    });

    refreshButton.addEventListener('click', async () => {
        loadResults()
    });

    columnsButton.addEventListener('click', async () => {
        const { modelName, questName } = getModelAndQuest();
        const { config, data } = await fetchData(modelName, questName);
        handleColumnsModal(config);
        filterColumns(config, data, modelName, questName);
    });

    searchForm.addEventListener('submit', async e => {
        e.preventDefault();
        const searchInput = document.querySelector('#search');
        const searchValue = searchInput.value;

        const { modelName, questName } = getModelAndQuest();
        const { config, data } = await fetchData(modelName, questName);

        let indexesFilter;
        if (searchValue) {
            indexesFilter = search(searchValue, data);
        }
        writeDataToTable(data, indexesFilter);
    });

    window.onclick = event => {
        if (event.target.matches('.columns-modal-background')) {
            const columnsModal = document.querySelector('.columns-modal-background');
            columnsModal.classList.remove('modal-open');
        }
    };
});

async function fetchData(modelName, questName) {
    const res = await fetch(`/api/data/${modelName}/${questName}`);
    const data = await res.json();
    return data;
}

function writeDataToTable({ headers1, headers2, rows }, indexesFilter = null) {
    const tableHeaders1 = document.querySelector('#table-headers-1');
    const tableHeaders2 = document.querySelector('#table-headers-2');
    const tableBody = document.querySelector('#table-body');

    tableHeaders1.innerHTML = headers1.map((header, index) => `<th colspan="${headers2[index].length}">${header}</th>`).join('');
    tableHeaders2.innerHTML = headers2.map(header => header.map(subheader => `<th>${subheader}</th>`).join('')).join('');

    let rowsHTML = '';

    // loop through each column
    for (let i = 0; i < Object.values(rows)[0].length; i++) {
        rowsHTML += '<tr>';

        if (indexesFilter !== null && !indexesFilter.includes(i)) {
            continue;
        }

        headers2.forEach((header, index) => {
            header.forEach(subheader => {
                rowsHTML += `<td>${rows[`${headers1[index]}.${subheader}`][i]}</td>`;
            });
        });

        rowsHTML += '</tr>';
    }

    tableBody.innerHTML = rowsHTML;
}

function getModelAndQuest() {
    const modelsListItems = document.querySelectorAll('.sidebar .parent-list li.model-name');
    const questsListItems = document.querySelectorAll('.sidebar .child-list li.quest-name');

    const activeModelIndex = localStorage.getItem('activeModelIndex');
    const activeQuestIndex = localStorage.getItem('activeQuestIndex');

    questsListItems[activeQuestIndex].classList.add('active');

    const modelName = modelsListItems[activeModelIndex].innerText;
    const questName = questsListItems[activeQuestIndex].innerText;

    return { modelName, questName };
}

async function loadResults() {
    const { modelName, questName } = getModelAndQuest();
    const { data } = await fetchData(modelName, questName);
    writeDataToTable(data);
}

function handleColumnsModal(configData) {
    const columnsModal = document.querySelector('.columns-modal-background');
    const columnsContainer = document.querySelector('#columns-container');

    columnsContainer.innerHTML = Object.keys(configData).map(header => {
        let html = `
            <div class="mb-3">
                <h5 class="fs-5 fw-bold">${header}</h5>
                <div class="ms-5">
        `;
        html += Object.keys(configData[header]).map(subheader => {
            const columnName = `${header}.${subheader}`;
            const isChecked = configData[header][subheader] === 'true' ? 'checked' : '';
            return `
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="${columnName}" id="${columnName}" ${isChecked}>
                        <label class="form-check-label" for="${columnName}">
                        ${subheader}
                        </label>
                    </div>
                `
        }).join('')

        html += `
                </div>
            </div>
        `;

        return html;
    }).join('');

    columnsModal.classList.add('modal-open');
}

function filterColumns(configData, data, modelName, questName) {
    const columnsCheckboxes = document.querySelectorAll('#columns-container .form-check-input');

    columnsCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', async e => {
            const { checked, value } = e.target;
            const [header, subheader] = value.split('.');

            configData[header][subheader] = checked ? "true" : "false";

            const res = await fetch(`/api/save-config-data/${modelName}/${questName}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    header,
                    subheader,
                    checked
                })
            });

            if (res.ok) {
                const { modelName, questName } = getModelAndQuest();
                const { data } = await fetchData(modelName, questName);
                writeDataToTable(data);
            }
        });
    });
}

function search(searchValue, { rows }) {
    let column, value, filterCondition;

    // Greater than or equal to
    if (searchValue.indexOf('>=') !== -1) {
        [column, value] = searchValue.split('>=');
        filterCondition = (cell, value) => cell >= value;
    }
    // Greater than
    else if (searchValue.indexOf('>') !== -1) {
        [column, value] = searchValue.split('>');
        filterCondition = (cell, value) => cell > value;
    }
    // Less than or equal to
    else if (searchValue.indexOf('<=') !== -1) {
        [column, value] = searchValue.split('<=');
        filterCondition = (cell, value) => cell <= value;
    }
    // Less than
    else if (searchValue.indexOf('<') !== -1) {
        [column, value] = searchValue.split('<');
        filterCondition = (cell, value) => cell < value;
    }
    // Equal to
    else if (searchValue.indexOf('==') !== -1) {
        [column, value] = searchValue.split('==');
        filterCondition = (cell, value) => cell == value;
    }
    // Not equal to
    else if (searchValue.indexOf('!=') !== -1) {
        [column, value] = searchValue.split('!=');
        filterCondition = (cell, value) => cell != value;
    }
    // Unsupported search condition
    else {
        alert('Unsupported search condition. Please use one of the following: (>, >=, <, <=, ==, !=)');
        return;
    }

    column = column.trim();
    value = value.trim();

    return rows[column].map((cell, index) => {
        if (filterCondition(cell, value)) {
            return index;
        }
    }).filter(index => index !== undefined);
}