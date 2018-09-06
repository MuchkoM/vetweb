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
    $("info").text((i, origText) => origText ? origText : "<Не указанно>");
    $(".autocomplete[name]").autocomplete({
        source: function (request, response) {
            let name = this.element.attr('name');
            console.log(name);
            switch (name) {
                case 'subspecies':
                    $.getJSON(ajax['subspecies'], {
                        term: request.term,
                        term_2: $(".autocomplete[name='species']").val()
                    }, response);
                    break;
                default:
                    $.getJSON(ajax[name], {
                        term: request.term,
                    }, response);
            }
        },
        select: function (event, ui) {
            let value = ui.item.value;
            let name = $(this).attr('name')
            if (name === 'owner') {
                $('#id_owner_id').val(value);
            }
            ui.item.value = ui.item.label;
        },
        minLength: 0,
    }).focus(function () {
        $(this).autocomplete("search", $(this).val());
    });
});