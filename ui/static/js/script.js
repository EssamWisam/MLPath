document.addEventListener('DOMContentLoaded', async () => {
    const refreshButton = document.querySelector('#refresh-button');
    const columnsButton = document.querySelector('#columns-button');
    const searchForm = document.querySelector('#search-form');

    const { data } = await fetchData();
    writeDataToTable(data);

    refreshButton.addEventListener('click', async () => {
        const { data } = await fetchData();
        writeDataToTable(data);
    });

    columnsButton.addEventListener('click', async () => {
        const { config, data } = await fetchData();
        handleColumnsModal(config);
        filterColumns(config, data);
    });

    searchForm.addEventListener('submit', e => {
        e.preventDefault();
        const searchInput = document.querySelector('#search');
        const searchValue = searchInput.value;

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

    // $('#results-table')
    //     .DataTable({
    //         paging: false,
    //         searching: false,
    //         scrollX: true,
    //         select: true,
    //     });
});

async function fetchData() {
    const res = await fetch('/api/data');
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

function handleColumnsModal(configData) {
    const columnsModal = document.querySelector('.columns-modal-background');
    const columnsContainer = document.querySelector('#columns-container');

    columnsContainer.innerHTML = Object.keys(configData).map(header => {
        return Object.keys(configData[header]).map(subheader => {
            const columnName = `${header}.${subheader}`;
            const isChecked = configData[header][subheader] === 'true' ? 'checked' : '';
            return `
                    <div class="form-check">
                        <input class="form-check-input" type="checkbox" value="${columnName}" id="${columnName}" ${isChecked}>
                        <label class="form-check-label" for="${columnName}">
                        ${columnName}
                        </label>
                    </div>
                `
        }).join('')
    }).join('');

    columnsModal.classList.add('modal-open');
}

function filterColumns(configData, data) {
    const columnsCheckboxes = document.querySelectorAll('#columns-container .form-check-input');

    columnsCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', async e => {
            const { checked, value } = e.target;
            console.log({ checked, value });
            const [header, subheader] = value.split('.');

            configData[header][subheader] = checked ? "true" : "false";

            const res = await fetch('/api/save-config-data', {
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
                const { data } = await fetchData();
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