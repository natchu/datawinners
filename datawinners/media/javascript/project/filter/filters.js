$.fn.datePicker = function (options) {
    return this.each(function () {
        var $this = $(this);
        var config = $.extend({
            'date_format': 'dd.mm.yyyy'
        }, options || {});
        var widget = $this.daterangepicker(getSettings(config, config.header || gettext('All Dates'), $this.data('ismonthly')))
        if ($this.data('ismonthly') != undefined) widget.monthpicker(options.monthpicker);
        $this.click(function () {
//            var $monthpicker = $('#monthpicker_start, #monthpicker_end', $('.ranges'));
//            if ($this.data('ismonthly')) {
//                $monthpicker.show();
//            } else {
//                $monthpicker.hide();
//            }
            var $visible_datepickers = $('.ui-daterangepicker:visible');
            $visible_datepickers.each(function (index, picker) {
                if ($(picker).data('for') != $this.attr('id')) {
                    $(picker).hide();
                }
            });
        });

        function getModifiedDateFormat(date_format) {
            return date_format.replace('yyyy', 'yy');
        }

        function getSettings(config, header, ismonthly) {
            var year_to_date_setting = {text: gettext('Year to date'), dateStart: function () {
                var x = Date.parse('today');
                x.setMonth(0);
                x.setDate(1);
                return x;
            }, dateEnd: 'today' };
            var settings = {
                presetRanges: [
                    {text: header, dateStart: function () {
                        return Date.parse('1900.01.01')
                    }, dateEnd: 'today', is_for_all_period: true },
                    {text: gettext('Current month'), dateStart: function () {
                        return Date.parse('today').moveToFirstDayOfMonth();
                    }, dateEnd: 'today' },
                    {text: gettext('Last Month'), dateStart: function () {
                        return Date.parse('last month').moveToFirstDayOfMonth();
                    }, dateEnd: function () {
                        return Date.parse('last month').moveToLastDayOfMonth();
                    } }
                ],
                presets: {dateRange: gettext('Choose Date(s)')},
                earliestDate: '1/1/2011',
                latestDate: '21/12/2012',
                dateFormat: getModifiedDateFormat(config.date_format),
                rangeSplitter: '-',
                closeOnSelect:false
            };
            if (ismonthly) {
                settings.presets = {dateRange: gettext('Choose Month(s)')}
            } else {
                settings.presetRanges = settings.presetRanges.concat(year_to_date_setting);
            }
            settings.eventCallback = config.eventCallback;
            settings.onClose = config.onCloseCallback;
            settings.monthpicker = config.monthpicker;
            return settings;
        }
    })
};

DW.get_datepicker_value = function ($datePicker, default_text) {
    var data = $datePicker.val().split("-");
    if (data[0] == "" || data[0] == default_text) {
        data = ['', ''];
    } else if (data[0] != default_text && Date.parse(data[0]) == null) {
        $datePicker.next().html('<label class=error>' + gettext("Enter a correct date. No filtering applied") + '</label>').show();
        data = ['', ''];
    } else if (data.length == 1) {
        data[1] = data[0];
    }
    return {start_time: data[0], end_time: data[1]};
};