$(function() {
    $('#add-form').click(function() {
        var formTemplate = document.getElementById('new-guest-form');
        var inputs = formTemplate.content.querySelectorAll("input");
        inputs.forEach(function(element) {
            element.name = element.name.replace('__prefix__', formCount);
        })
        var form = document.importNode(formTemplate.content, true);
        $('#guests').append(form);
        formCount++;
        $('#id_guests-TOTAL_FORMS').val(formCount);
    });
});
