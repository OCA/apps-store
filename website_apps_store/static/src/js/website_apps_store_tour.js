odoo.define("website_apps_store.tour_custom", function (require) {
    "use strict";

    var Tour = require("web_tour.tour");
    var base = require("web_editor.base");

    Tour.register(
        "successfully_download_zip",
        {
            name: "Download Zip File - successfully",
            url: "/shop/page/2",
            test: true,
            wait_for: base.ready(),
        },
        [
            {
                content: "Shop",
                trigger: ".oe_product_cart a:contains('Odoo Module')",
            },
            {
                content: "Select Version",
                trigger: "input[type=radio]",
                run: function () {
                    $("input[type=radio]:last").attr("checked", "checked");
                },
            },
            {
                content: "Download",
                trigger: "#download_zip",
            },
            {
                content: "No failure, we are in the same page",
                trigger: "#product_detail",
            },
        ]
    );

    Tour.register(
        "download_zip_failed",
        {
            name: "Download Zip File - Failed",
            url: "/shop/page/2",
            test: true,
            wait_for: base.ready(),
        },
        [
            {
                content: "Shop",
                trigger: ".oe_product_cart a:contains('Odoo Module')",
            },
            {
                content: "Select Version",
                trigger: "input[type=radio]",
                run: function () {
                    $("input[type=radio]:last").attr("checked", "checked");
                },
            },
            {
                content: "Download",
                trigger: "#download_zip",
            },
            {
                content: "Suspicious",
                trigger: "#wrap.wrap-download-zip-failed",
            },
        ]
    );

    Tour.register(
        "select_version_search",
        {
            name: "Select Version",
            url: "/shop",
            test: true,
            wait_for: base.ready(),
        },
        [
            {
                content: "Shop",
                trigger: ".dropdown_version_by a.dropdown-toggle",
            },
            {
                content: "Select Version",
                trigger: ".dropdown_version_by .dropdown-menu a:contains('10.0')",
            },
        ]
    );

    Tour.register(
        "select_category_search",
        {
            name: "Select Category",
            url: "/shop",
            test: true,
            wait_for: base.ready(),
        },
        [
            {
                content: "Shop",
                trigger: ".dropdown_category_by a.dropdown-toggle",
            },
            {
                content: "Select Category",
                trigger: ".dropdown_category_by .dropdown-menu a:contains('Category')",
            },
        ]
    );

    Tour.register(
        "module_search",
        {
            name: "Select Product(Module)",
            url: "/shop",
            test: true,
            wait_for: base.ready(),
        },
        [
            {
                content: "Shop",
                trigger: ".search-query",
                run: function () {
                    $(".search-query").attr("value", "Test");
                },
            },
            {
                content: "Search Button",
                trigger: ".oe_search_button",
            },
            {
                content: "There is one or more products as a search result",
                trigger: "#products_grid td.oe_product a:contains('Odoo Module')",
            },
        ]
    );

    Tour.register(
        "technical_name_search",
        {
            name: "Select Product(Module) by Technical Name",
            url: "/shop",
            test: true,
            wait_for: base.ready(),
        },
        [
            {
                content: "Shop",
                trigger: ".search-query",
                run: function () {
                    $(".search-query").attr("value", "odoo_module");
                },
            },
            {
                content: "Search Button",
                trigger: ".oe_search_button",
            },
            {
                content: "There is one or more products as a search result",
                trigger: "#products_grid td.oe_product a:contains('Odoo Module')",
            },
        ]
    );
});
