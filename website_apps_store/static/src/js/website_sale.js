/**
*    Copyright 2018 BizzAppDev
*    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

odoo.define('website_apps_store.website_sale', function (require) {
    'use strict';

    require('web.dom_ready');
    var base = require("web_editor.base");
    var ajax = require('web.ajax');
    var utils = require('web.utils');
    var core = require('web.core');
    var config = require('web.config');
    require("website.content.zoomodoo");
    var _t = core._t;


    $('.oe_website_sale').each(function () {
        var oe_website_sale = this;
        var $product_global;

        function price_to_str(price) {
            var l10n = _t.database.parameters;
            var precision = 2;

            if ($(".decimal_precision").length) {
                precision = parseInt($(".decimal_precision").last().data('precision'));
            }
            var formatted = _.str.sprintf('%.' + precision + 'f', price).split('.');
            formatted[0] = utils.insert_thousand_seps(formatted[0]);
            return formatted.join(l10n.decimal_point);
        }


        function update_product_image(event_source, product_id) {
            var $img;
            if ($('#o-carousel-product').length) {
                $img = $(event_source).closest('tr.js_product, .oe_website_sale').find('img.js_variant_img');
                $img.attr("src", "/web/image/product.product/" + product_id + "/image");
                $img.parent().attr('data-oe-model', 'product.product').attr('data-oe-id', product_id)
                    .data('oe-model', 'product.product').data('oe-id', product_id);

                var $thumbnail = $(event_source).closest('tr.js_product, .oe_website_sale').find('img.js_variant_img_small');
                if ($thumbnail.length !== 0) { // if only one, thumbnails are not displayed
                    $thumbnail.attr("src", "/web/image/product.product/" + product_id + "/image/90x90");
                    $('.carousel').carousel(0);
                }
            }
            else {
                $img = $(event_source).closest('tr.js_product, .oe_website_sale').find('span[data-oe-model^="product."][data-oe-type="image"] img:first, img.product_detail_img');
                $img.attr("src", "/web/image/product.product/" + product_id + "/image");
                $img.parent().attr('data-oe-model', 'product.product').attr('data-oe-id', product_id)
                    .data('oe-model', 'product.product').data('oe-id', product_id);
            }
            // reset zooming constructs
            $img.filter('[data-zoom-image]').attr('data-zoom-image', $img.attr('src'));
            if ($img.data('zoomOdoo') !== undefined) {
                $img.data('zoomOdoo').isReady = false;
            }
        }

        $(oe_website_sale).on('change', 'input.js_variant_change, select.js_variant_change, ul[data-attribute_value_ids]', function (ev) {
            var $ul = $(ev.target).closest('.js_add_cart_variants');
            var $parent = $ul.closest('.js_product');
            var $product_id = $parent.find('.product_id').first();
            var $price = $parent.find(".oe_price:first .oe_currency_value");
            var $default_price = $parent.find(".oe_default_price:first .oe_currency_value");
            var $tech_deatil = $(".tech_deatil");
            var $license_detail = $(".license_detail");
            var $license_url = $(".license_url");
            var $author_detail = $(".author_detail");
            var $website_detail = $(".website_detail");
            var $repo_detail = $(".repo_detail");
            var $rst_html = $(".desc_rst");
            var $app_summary = $(".app_summary");
            var $name_product = $(".name_product");
            var $optional_price = $parent.find(".oe_optional:first .oe_currency_value");
            var variant_ids = $ul.data("attribute_value_ids");
            if(_.isString(variant_ids)) {
                variant_ids = JSON.parse(variant_ids.replace(/'/g, '"'));
            }
            var values = [];
            var unchanged_values = $parent.find('div.oe_unchanged_value_ids').data('unchanged_value_ids') || [];

            $parent.find('input.js_variant_change:checked, select.js_variant_change').each(function () {
                values.push(+$(this).val());
            });
            values =  values.concat(unchanged_values);

            $parent.find("label").removeClass("text-muted css_not_available");

            var product_id = false;
            for (var k in variant_ids) {
                if (_.isEmpty(_.difference(variant_ids[k][1], values))) {
                    $.when(base.ready()).then(function() {
                        $price.html(price_to_str(variant_ids[k][2]));
                        $default_price.html(price_to_str(variant_ids[k][3]));
                    });
                    if (variant_ids[k][3]-variant_ids[k][2]>0.01) {
                        $default_price.closest('.oe_website_sale').addClass("discount");
                        $optional_price.closest('.oe_optional').show().css('text-decoration', 'line-through');
                        $default_price.parent().removeClass('hidden');
                    } else {
                        $optional_price.closest('.oe_optional').hide();
                        $default_price.parent().addClass('hidden');
                    }
                    product_id = variant_ids[k][0];
                    $product_global = product_id;
                    update_product_image(this, product_id);
                    ajax.jsonRpc("/shop/change_attribute_version", 'call', {
                        'product_id': product_id,
                    }).then(function (data) {
                        if(data){
                            $tech_deatil.text(data['technical_name']);
                            $license_detail.text(data['license']);
                            $('.license_url').attr('href', data['license_url']);
                            $author_detail.text(data['author']);
                            $website_detail.text(data['website']);
                            $repo_detail.text(data['repository']);
                            $repo_detail.parent()[0].href = data['repository'];
                            $rst_html.html(data['rst_html']);
                            $app_summary.text(data['app_summary']);
                            $name_product.text(data['name_product']);
                        }
                    });
                    break;
                }
            }

            $parent.find("input.js_variant_change:radio, select.js_variant_change").each(function () {
                var $input = $(this);
                var id = +$input.val();
                var values = [id];

                $parent.find("ul:not(:has(input.js_variant_change[value='" + id + "'])) input.js_variant_change:checked, select.js_variant_change").each(function () {
                    values.push(+$(this).val());
                });

                for (var k in variant_ids) {
                    if (!_.difference(values, variant_ids[k][1]).length) {
                        return;
                    }
                }
                $input.closest("label").addClass("css_not_available");
                $input.find("option[value='" + id + "']").addClass("css_not_available");
            });

            if (product_id) {
                $parent.removeClass("css_not_available");
                $product_id.val(product_id);
                $parent.find("#add_to_cart").removeClass("disabled");
            } else {
                $parent.addClass("css_not_available");
                $product_id.val(0);
                $parent.find("#add_to_cart").addClass("disabled");
            }
        });

        $('#download_zip').on('click', function(ev){
          var product_template_id = $(this).data('tmpl-id');
          ev.preventDefault();
          var google_captcha = $('#g-recaptcha-response').val();
          if (!google_captcha)
            return ;
          if (grecaptcha !== 'undefined'){
            grecaptcha.reset();
          }
          if ($product_global){
              window.location.href = "/shop/download_product_zip/" + product_template_id + '/' + $product_global + '/' + google_captcha;
          }else{
              window.location.href = "/shop/download_product_zip/" + product_template_id + '/' + google_captcha;
          }
        });
      var $captchas = $('.o_website_form_recaptcha');
        ajax.post('/website/recaptcha/', {}).then(
            function (result) {
                var data = JSON.parse(result);
                $captchas.append($(
                    '<div class="g-recaptcha" data-sitekey="' + data.site_key + '"></div>'
                ));
                if ($captchas.length) {
                    $.getScript('https://www.google.com/recaptcha/api.js');
                }
            }
        );
    });
});
