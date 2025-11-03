/** @odoo-module **/

import {registry} from "@web/core/registry";

const tour = registry.category("web_tour.tours");

tour.add("successfully_download_zip", {
    name: "Download Zip File - successfully",
    url: "/shop/page/2",
    test: true,
    steps: [
        {
            content: "Shop",
            trigger: ".oe_product_cart a:contains('Odoo Module')",
            run: "click",
        },
        {
            content: "Select Version",
            trigger: "input[type=radio]",
            run() {
                const radios = document.querySelectorAll("input[type='radio']");
                if (radios.length) {
                    radios[radios.length - 1].checked = true;
                }
            },
        },
        {
            content: "Download",
            trigger: "#download_zip",
            run: "click",
        },
        {
            content: "No failure, we are in the same page",
            trigger: "#product_detail",
        },
    ],
});

tour.add("download_zip_failed", {
    name: "Download Zip File - Failed",
    url: "/shop/page/2",
    test: true,
    steps: [
        {
            content: "Shop",
            trigger: ".oe_product_cart a:contains('Odoo Module')",
            run: "click",
        },
        {
            content: "Select Version",
            trigger: "input[type=radio]",
            run() {
                const radios = document.querySelectorAll("input[type='radio']");
                if (radios.length) {
                    radios[radios.length - 1].checked = true;
                }
            },
        },
        {
            content: "Download",
            trigger: "#download_zip",
            run: "click",
        },
        {
            content: "Suspicious",
            trigger: "#wrap.wrap-download-zip-failed",
        },
    ],
});

tour.add("select_version_search", {
    name: "Select Version",
    url: "/shop",
    test: true,
    steps: [
        {
            content: "Shop",
            trigger: ".dropdown_version_by a.dropdown-toggle",
            run: "click",
        },
        {
            content: "Select Version",
            trigger: ".dropdown_version_by .dropdown-menu a:contains('10.0')",
            run: "click",
        },
    ],
});

tour.add("select_category_search", {
    name: "Select Category",
    url: "/shop",
    test: true,
    steps: [
        {
            content: "Shop",
            trigger: ".dropdown_category_by a.dropdown-toggle",
            run: "click",
        },
        {
            content: "Select Category",
            trigger: ".dropdown_category_by .dropdown-menu a:contains('Category')",
            run: "click",
        },
    ],
});

tour.add("module_search", {
    name: "Select Product(Module)",
    url: "/shop",
    test: true,
    steps: [
        {
            content: "Shop",
            trigger: ".search-query",
            run() {
                const el = document.querySelector(".search-query");
                if (el) el.value = "Test";
            },
        },
        {
            content: "Search Button",
            trigger: ".oe_search_button",
            run: "click",
        },
        {
            content: "There is one or more products as a search result",
            trigger: "#products_grid td.oe_product a:contains('Odoo Module')",
        },
    ],
});

tour.add("technical_name_search", {
    name: "Select Product(Module) by Technical Name",
    url: "/shop",
    test: true,
    steps: [
        {
            content: "Shop",
            trigger: ".search-query",
            run() {
                const el = document.querySelector(".search-query");
                if (el) el.value = "odoo_module";
            },
        },
        {
            content: "Search Button",
            trigger: ".oe_search_button",
            run: "click",
        },
        {
            content: "There is one or more products as a search result",
            trigger: "#products_grid td.oe_product a:contains('Odoo Module')",
        },
    ],
});
