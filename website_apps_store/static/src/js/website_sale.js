/* global grecaptcha */
/**
*    Copyright 2018 BizzAppDev
*    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

odoo.define('website_apps_store.website_sale', function (require) {
    'use strict';

    require('web.dom_ready');
    var ajax = require('web.ajax');
    var sAnimations = require('website.content.snippets.animation');
    var WebsiteSale = sAnimations.registry.WebsiteSale;

    WebsiteSale.include({
        read_events: _.extend({}, WebsiteSale.prototype.read_events, {
            'click #download_zip': '_onClickDownload',
        }),

        init: function () {
            this._super.apply(this, arguments);
            var $captchas = $('.o_website_form_recaptcha');
            ajax.post('/website/recaptcha/', {}).then(
                function (result) {
                    var data = JSON.parse(result);
                    $captchas.append($(
                        '<div class="g-recaptcha" data-sitekey="' +
                        data.site_key + '"></div>'
                    ));
                    if ($captchas.length) {
                        $.getScript('https://www.google.com/recaptcha/api.js');
                    }
                }
            );
        },

        _onChangeCombination: function (ev, $parent, combination) {
            this._super.apply(this, arguments);
            if ('is_odoo_module' in combination && combination.is_odoo_module) {
                var $tech_deatil = this.$(".tech_deatil");
                var $license_detail = this.$(".license_detail");
                var $license_url = this.$(".license_url");
                var $author_detail = this.$(".author_detail");
                var $website_detail = this.$(".website_detail");
                var $repo_detail = this.$(".repo_detail");
                var $rst_html = this.$(".desc_rst");
                var $app_summary = this.$(".app_summary");
                var $name_product = this.$(".name_product");

                $tech_deatil.text(combination.technical_name);
                $license_detail.text(combination.license);
                $license_url.attr('href', combination.license_url);
                $author_detail.text(combination.author);
                $website_detail.text(combination.website);
                $repo_detail.text(combination.repository);
                $repo_detail.parent()[0].href = combination.repository;
                $rst_html.html(combination.rst_html);
                $app_summary.text(combination.app_summary);
                $name_product.text(combination.name_product);
            }
        },

        _onClickDownload: function (ev) {
            var $product_template_id = this.$('.product_template_id');
            var product_template_id = $product_template_id.val();
            var $product_id = this.$('.product_id');
            var product_id = $product_id.val();
            ev.preventDefault();
            var google_captcha = $('#g-recaptcha-response').val();
            if (!google_captcha) {
                return;
            }
            if (typeof grecaptcha !== 'undefined') {
                grecaptcha.reset();
            }
            if (product_id) {
                window.location.href = "/shop/download_product_zip/" +
                    product_template_id + '/' + product_id + '/' +
                    google_captcha;
            } else {
                window.location.href = "/shop/download_product_zip/" +
                    product_template_id + '/' + google_captcha;
            }
        },
    });
});
