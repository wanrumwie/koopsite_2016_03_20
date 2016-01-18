/*global $, test, equal */

test("errors should be hidden on keypress", function () {
    $('input').trigger('keypress');
    equal($('.has-error').is(':visible'), false);
});
test("errors not be hidden unless there is a keypress", function () {
    equal($('.has-error').is(':visible'), true);
});
