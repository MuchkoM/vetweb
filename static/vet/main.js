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
    $(".datepicker").datepicker({
        showOtherMonths: true,
        selectOtherMonths: true,
        showButtonPanel: true,
        changeMonth: true,
        changeYear: true,
    });
    $(".age").text(function (i, origText) {
        moment.locale('ru');
        let birth = moment(origText, "DD MMM YYYY");
        let now = moment();
        let year = now.diff(birth, 'year');
        let month = now.diff(birth, 'month') % 12;
        return ((year) ? getRusStringYear(year) : '') + ' ' + getRusStringMonth(month);
    });
    $(".autocomplete[name='owner']").autocomplete({
        source: autocomplete_owner,
        minLength: 0,
    }).focus(function () {
        $(this).autocomplete("search", $(this).val());
    });

    $(".autocomplete[name='animal']").autocomplete({
        source: autocomplete_animal,
        minLength: 0,
    }).focus(function () {
        $(this).autocomplete("search", $(this).val());
    });

    $(".autocomplete[name='species']").autocomplete({
        source: autocomplete_species,
        minLength: 0,
    }).focus(function () {
        $(this).autocomplete("search", $(this).val());
    });

    $(".autocomplete[name='vaccination']").autocomplete({
        source: autocomplete_vaccination,
        minLength: 0,
    }).focus(function () {
        $(this).autocomplete("search", $(this).val());
    });

    $(".autocomplete[name='subspecies']").autocomplete({
        source: function (request, response) {
            $.getJSON(autocomplete_subspecies, {
                term: request.term,
                term_2: $(".autocomplete[name='species']").val()
            }, response);
        },
        minLength: 0,
    }).focus(function () {
        $(this).autocomplete("search", $(this).val());
    });
});