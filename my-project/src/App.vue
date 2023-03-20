<template>
    <div class="container-fluid">
        <label>月份：
            <wj-combo-box :initialized="initMonthCombo" :itemsSource="month"
                :selectedIndexChanged="onMonthSelectedIndexChanged"></wj-combo-box>
        </label>
        <label>计算状态：</label>
        <label>{{ calStatus }}</label>
        <label><v-btn style="border: 1px solid black; background-color: white;" @click="btn_cal">计算</v-btn></label>
        <label>查询方案编号：
            <wj-combo-box :initialized="initQueryCodeCombo" :itemsSource="queryCode"
                :selectedIndexChanged="onQueryCodeSelectedIndexChanged"></wj-combo-box>
        </label>
        <label><v-btn style="border: 1px solid black; background-color: white;" @click="btn_query">查询</v-btn></label>
        <wj-flex-grid id="grid" :itemsSource="gridView" :allowMerging="'All'" :initialized="onInitialized"></wj-flex-grid>
    </div>
</template>

<script>
import "@grapecity/wijmo.styles/wijmo.css";
import "bootstrap.css";
import Vue from "vue";

import * as wjCore from "@grapecity/wijmo";
import * as wjGrid from "@grapecity/wijmo.grid";
import "@grapecity/wijmo.vue2.input";
import "@grapecity/wijmo.vue2.grid";

import { getMonths, getQueryCodes, getStrLen } from "./data";

let App = Vue.extend({
    name: "app",

    data: function () {
        return {
            month: getMonths(),
            queryCode: getQueryCodes(),
            calStatus: "未知",
            gridData: null,
            gridView: null,

            gridLoaded: false,

            cols: null,
        };

    },
    methods: {
        initMonthCombo: function (monthCombo) {
            this.monthCombo = monthCombo;
        },
        onMonthSelectedIndexChanged: function () {
            console.log(this.monthCombo.text)
            fetch('http://127.0.0.1:8085/get_caled', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ month: this.monthCombo.text })
            })
                .then(response => response.json())
                .then(data => this.calStatus = data["status"])
                .catch(error => console.error(error));
        },

        btn_cal() {
            console.log("计算逻辑");
        },

        initQueryCodeCombo: function (queryCodeCombo) {
            this.queryCodeCombo = queryCodeCombo;
        },
        onQueryCodeSelectedIndexChanged: function () {

        },


        btn_query() {
            fetch('http://127.0.0.1:8085/get_query_data', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ month: this.monthCombo.text, query_code: this.queryCodeCombo.text })
            })
                .then(response => response.json())
                .then(data => {
                    console.log(data)

                    this.gridData = data;
                    this.gridView = new wjCore.CollectionView(this.gridData);

                })
                .then(empty => {
                    var panel = this.grid.columnHeaders;

                    if (this.gridLoaded == false) {
                        var extraRow1 = new wjGrid.Row();
                        extraRow1.allowMerging = true;
                        panel.rows.splice(0, 0, extraRow1);

                        var extraRow2 = new wjGrid.Row();
                        extraRow2.allowMerging = true;
                        panel.rows.splice(1, 0, extraRow2);

                        var extraRow3 = new wjGrid.Row();
                        extraRow3.allowMerging = true;
                        panel.rows.splice(2, 0, extraRow3);

                        this.gridLoaded = true;
                    }

                    var cols = [];
                    fetch('http://127.0.0.1:8085/get_query_cols', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ month: this.monthCombo.text, query_code: this.queryCodeCombo.text })
                    })
                        .then(response => response.json())
                        .then(data => {
                            this.cols = [];
                            console.log("done")
                            for (let col of data) {
                                cols.push(col);
                                this.cols.push(col);
                            }
                            console.log(this.cols);
                        })
                        .then(empty => {
                            var first = ""
                            var second = ""
                            for (let col of cols) {
                                let _col = this.grid.getColumn(col);
                                if (_col == null)
                                    continue;
                                _col.allowMerging = true;
                                let index = col.indexOf("_")
                                if (index == -1) {
                                    panel.setCellData(0, _col.index, _col.header);
                                    panel.setCellData(1, _col.index, _col.header);
                                    panel.setCellData(2, _col.index, _col.header);
                                }
                                else {
                                    first = col.substr(0, index)
                                    col = col.substr(index + 1)
                                    index = col.indexOf("_")
                                    second = col.substr(0, index)
                                    col = col.substr(index + 1)
                                    _col.header = col;
                                    panel.setCellData(0, _col.index, "成本项目");
                                    panel.setCellData(1, _col.index, first);
                                    panel.setCellData(2, _col.index, second);
                                }
                                
                                var maxLen = getStrLen(col);
                                for (let i = 0; i < panel.rows.length; i++) {
                                    let cell = this.grid.getCellData(i, _col.index, true);
                                    let len = getStrLen(cell);
                                    if (len > maxLen)
                                        maxLen = len;
                                }
                                _col.width = maxLen * 7 + 50;

                                this.grid.formatItem.addHandler(centerCell);
                                console.log(this.cols);
                            }
                        })
                        .catch(error => console.error(error));
                })
                .catch(error => console.error(error));
        },

        onInitialized(grid) {
            grid.mergeManager = new CustMergeManager(grid);
            this.grid = grid;
        },

        getData: function () {
            var data = [];

            return data;
        },
    },

    mounted: function () {
        this.gridData = this.getData();
        this.gridView = new wjCore.CollectionView(this.gridData);
    },
});

var CustMergeManager = (function (_super) {
    __extends(CustMergeManager, _super);
    function CustMergeManager(flexGrid) {
        return _super.call(this, flexGrid) || this;
    }
    CustMergeManager.prototype.getMergedRange = function (p, r, c, clip) {
        if (clip === void 0) {
            clip = true;
        }
        var rng = null;
        rng = new wjGrid.CellRange(r, c);
        // var pcol = c > 0 ? c - 1 : c;
        // var val = p.getCellData(r, c, false);
        // var pval = p.getCellData(r, pcol, false);
        // while (
        //     rng.row > 0 &&
        //     p.getCellData(rng.row - 1, c, false) == val &&
        //     p.getCellData(rng.row - 1, pcol, false) == pval
        // ) {
        //     rng.row--;
        // }
        // while (
        //     rng.row2 < p.rows.length - 1 &&
        //     p.getCellData(rng.row2 + 1, c, false) == val &&
        //     p.getCellData(rng.row2 + 1, pcol, false) == pval
        // ) {
        //     rng.row2++;
        // }
        console.log(this.cols);
        if (this.cols != null) {
            console.log(this.cols[c]);
        }
        if (rng.isSingleCell) {
            rng = null;
        }
        //console.log(rng);
        return rng;
    };
    return CustMergeManager;
})(wjGrid.MergeManager);

function centerCell(s, e) {
    if (e.cell.children.length == 0) {
        e.cell.innerHTML = "<div>" + e.cell.innerHTML + "</div>";
        wjCore.setCss(e.cell, {
            display: "table",
            tableLayout: "fixed"
        });
        wjCore.setCss(e.cell.children[0], {
            display: "table-cell",
            textAlign: "center",
            verticalAlign: "middle"
        });
    }
}

new Vue({ render: h => h(App) }).$mount("#app");
</script>

<style>
.wj-flexgrid {
    max-height: 490px;
}

#grid.wj-flexgrid .wj-cell {
    padding: 0px;
}

body {
    margin-bottom: 24pt;
}
</style>