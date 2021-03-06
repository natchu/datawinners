/* Value Labels Plugin for flot.
 * Homepage:
 * http://sites.google.com/site/petrsstuff/projects/flotvallab
 *
 * Released under the MIT license by Petr Blahos, December 2009.
 *
 */
(function ($) {
    var options = {
        valueLabels: {
            show: false
        }
    };

    function init(plot) {
        plot.hooks.draw.push(function (plot, ctx) {
            if (!plot.getOptions().valueLabels.show) {
                return
            }
            $.each(plot.getData(), function(ii, series) {
                plot.getPlaceholder().find("#valueLabels"+ii).remove();
                var html = '<div id="valueLabels' + series.seriesIndex + '" class="valueLabels">';
                var last_val = null;
                var last_x = -1000;
                var last_y = -1000;
                for (var i = 0; i < series.data.length; ++i) {
                    if (series.data[i] == null) {
                        continue;
                    }

                    var x = series.data[i][0], y = series.data[i][1];
                    if (x < series.xaxis.min || x > series.xaxis.max || y < series.yaxis.min || y > series.yaxis.max) {
                        continue;
                    }
                    var val = x;
                    if (series.valueLabelFunc) {
                        val = series.valueLabelFunc({ series: series, seriesIndex: ii, index: i });
                    }
                    val = ""+val;
                    if (true) {
                        var xx = series.xaxis.p2c(x)+plot.getPlotOffset().left;
                        var yy = series.yaxis.p2c(y)-12+plot.getPlotOffset().top;
                        if (Math.abs(yy-last_y)>20 || last_x<xx) {
                            last_val = val;
                            last_x = xx + val.length*8;
                            last_y = yy;
                            var head = '<div style="left:' + xx + 'px;top:' + yy + 'px;" class="valueLabel';
                            var tail = '">' + val + '</div>';
                            html+= head + "Light" + tail + head + tail;
                        }
                    }
                }
                html+= "</div>";
                plot.getPlaceholder().append(html);
            });
        });
    }

    $.plot.plugins.push({
        init: init,
        options: options,
        name: 'valueLabels',
        version: '1.0'
    });
})(jQuery);
