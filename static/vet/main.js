function getRusStringNumber(value, strList) {
    let mod = value % 10;
    let loc_string;
    if (value < 20 && value > 11) {
        loc_string = strList[2]
    } else {
        if (mod === 1) {
            loc_string = strList[0];
        } else if (mod > 1 && mod < 5) {
            loc_string = strList[1];
        } else {
            loc_string = strList[2];
        }
    }
    return value + ' ' + loc_string
}

function getRusStringYear(year) {
    return getRusStringNumber(year, ['год', 'года', 'лет'])
}

function getRusStringMonth(month) {
    return getRusStringNumber(month, ['месяц', 'месяца', 'месяцев'])
}

$(function () {
    $.datepicker.setDefaults($.datepicker.regional['ru']);
    moment.locale('ru');
    $(".datepicker").datepicker({
        showOtherMonths: true,
        selectOtherMonths: true,
        showButtonPanel: true,
        changeMonth: true,
        changeYear: true,
    });
    $("age").text(function (i, origText) {
        let birth = moment(origText, "DD MMM YYYY");
        let now = moment();
        let year = now.diff(birth, 'year');
        let month = now.diff(birth, 'month') % 12;
        return ((year) ? getRusStringYear(year) : '') + ' ' + getRusStringMonth(month);
    });
    $("info").text(function (i, origText) {
        if (origText)
            return origText;
        else
            return "<Не указанно>"
    });
    $(".autocomplete[name]").autocomplete({
        source: function (request, response) {
            let name = this.element.attr('name');
            if (name === 'subspecies') {
                $.getJSON(ajax['subspecies'], {
                    term: request.term,
                    term_2: $(".autocomplete[name='species']").val()
                }, response);
            } else {
                $.getJSON(ajax[name], {
                    term: request.term,
                }, response);
            }
        },
        minLength: 0,
    }).focus(function () {
        $(this).autocomplete("search", $(this).val());
    });
});