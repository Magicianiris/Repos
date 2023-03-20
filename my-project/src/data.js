export function getMonths() {
    let months = [getDefaultMonth()];

    fetch('http://127.0.0.1:8085/get_months', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            for (let month of data) {
                if (month == getDefaultMonth())
                    continue;
                months.push(month);
            }
        })
        .catch(error => console.error(error));

    return months;
}

export function getQueryCodes() {
    let cols = [getDefaultQueryCode()];

    fetch('http://127.0.0.1:8085/get_query_codes', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            for (let col of data) {
                if (col == getDefaultQueryCode())
                    continue;
                cols.push(col);
            }
        })
        .catch(error => console.error(error));

    return cols;
}


function getDefaultMonth() {
    var date = new Date();
    return date.getFullYear().toString() + fixZeroStart(fixZeroStart((date.getMonth() + 1).toString(), 2));
}
function fixZeroStart(str, n) {
    return (Array(n).join(0) + str).slice(-n);
}

function getDefaultQueryCode(str, n) {
    return '0101';
}

export function getStrLen(str) {
    var strlen = 0;
    for (var i = 0; i < str.length; i++) {
        if (str.charCodeAt(i) > 255) //如果是汉字，则字符串长度加2
            strlen += 2;
        else
            strlen++;
    }
    return strlen;
}
