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
    $("span.age").text(function (i, origText) {
        let birth = moment(origText, "DD MMM YYYY");
        let now = moment();
        let year = now.diff(birth, 'year');
        let month = now.diff(birth, 'month') % 12;
        return ((year) ? getRusStringYear(year) : '') + ' ' + getRusStringMonth(month);
    });
    $("span.info").text((i, origText) => origText ? origText : "<Не указанно>");
    $(".autocomplete[name]").autocomplete({
        source: function (request, response) {
            let name = this.element.attr('name');//WHY??? this is place do same thing like other
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
            let name = $(this).attr('name');//WHY??? this is place do same thing like other
            if (name === 'owner') {
                $('#id_owner_id').val(value);
            }
            ui.item.value = ui.item.label;
        },
        minLength: 0,
    }).focus(function () {
        $(this).select();
        $(this).autocomplete("search", $(this).val());
    });
    $('#topNavBar .nav-link[href="' + window.location.pathname + '"]').parent().addClass('active');
    $('table[data-model-name] button.add').click(function () {
        let type = $(this).parents('table').attr('data-model-name');
        let $tr = $(this).parents('tr');
        let url = url_accelerate[type]['create'];
        let content;
        switch (type) {
            case 'subspecies':
                content = {
                    "species": $tr.children().eq(0).text(),
                    'subspecies': $tr.children().eq(1).text()
                };
                break;
            default:
                content = {
                    "value": $tr.children().eq(0).text()
                };
        }
        $.get(url, content, function (result) {
            if ('error' in result) {
                $('#status_msg').css("color", "red").text("Ошибка при добавлении");
            } else {
                $('#status_msg').css("color", "green").text("Добавление успешно");
                location.reload();
            }
        });
    });
    $('table[data-model-name] button.update').click(function () {
        let type = $(this).parents('table').attr('data-model-name');
        let $tr = $(this).parents('tr');
        let pk = $tr.attr('id');
        let url = url_accelerate[type]['update'] + pk;
        let content;
        switch (type) {
            case 'subspecies':
                content = {
                    "species": $tr.children().eq(0).text(),
                    'subspecies': $tr.children().eq(1).text()
                };
                break;
            default:
                content = {
                    "value": $tr.children().eq(0).text()
                };
        }
        $.get(url, content, function (result) {
            if ('error' in result) {
                $('#status_msg').css("color", "red").text("Ошибка при обновлении");
            } else {
                $('#status_msg').css("color", "green").text("Обновление успешно");
            }
        });
    });
    $('table[data-model-name] button.delete').click(function () {
        let type = $(this).parents('table').attr('data-model-name');
        let $tr = $(this).parents('tr');
        let pk = $tr.attr('id');
        let url = url_accelerate[type]['delete'] + pk;
        $.get(url, function (result) {
            if ('error' in result) {
                $('#status_msg').css("color", "red").text("Ошибка при удалении");
            } else {
                $('#status_msg').css("color", "green").text("Удаление успешно");
                location.reload();
            }
        });
    });
});