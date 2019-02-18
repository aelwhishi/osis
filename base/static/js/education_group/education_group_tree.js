function switchTreeVisibility() {
    var newTreeVisibility = (sessionStorage.getItem('treeVisibility') === '0') ? '1' : '0';
    sessionStorage.setItem('treeVisibility', newTreeVisibility);
    showOrHideTree()
}

function showOrHideTree() {
    if (sessionStorage.getItem('treeVisibility') === "0") {
        modifyPanelAttribute("none", "col-md-0", "col-md-12");
    } else {
        modifyPanelAttribute("block", "col-md-3", "col-md-9");
    }
}


function modifyPanelAttribute(collapse_style_display, panel_collapse_class, panel_data_class) {
    document.getElementById('collapse').style.display = collapse_style_display;
    document.getElementById('panel-collapse').className = panel_collapse_class;
    document.getElementById('panel-data').className = panel_data_class;
}


$(document).ready(function () {
    var $documentTree = $('#panel_file_tree');

    $documentTree.bind("state_ready.jstree", function (event, data) {

        // Bind the redirection only when the tree is ready,
        // however, it reload the page during the loading
        $documentTree.bind("select_node.jstree", function (event, data) {
            document.location.href = data.node.a_attr.href;
        });

        // if the tree has never been loaded, execute open_all by default.
        if ($.vakata.storage.get(data.instance.settings.state.key) === null) {
            $(this).jstree('open_all');
        }
    });

    function get_data_from_tree(data) {
        var inst = $.jstree.reference(data.reference),
            obj = inst.get_node(data.reference);

        return {
            group_element_year_id: obj.a_attr.group_element_year,
            element_id: obj.a_attr.element_id,
            element_type: obj.a_attr.element_type,
            has_prerequisite: obj.a_attr.has_prerequisite,
            is_prerequisite: obj.a_attr.is_prerequisite,
            attach_url: obj.a_attr.attach_url,
            detach_url: obj.a_attr.detach_url
        };
    }

    function build_url_data(element_id, group_element_year_id, action) {
        var data = {
            'root_id': root_id,
            'element_id': element_id,
            'group_element_year_id': group_element_year_id,
            'action': action,
            'source': url_resolver_match
        };
        return jQuery.param(data);
    }

    $documentTree.jstree({
            "core": {
                "check_callback": true,
                "data": tree,
            },
            "plugins": [
                "contextmenu",
                // Plugin to save the state of the node (collapsed or not)
                "state",
            ],
            "state": {
                // the key is important if you have multiple trees in the same domain
                // The key includes the root_id
                "key": location.pathname.split('/', 3).join('/'),
                "opened": true,
                "selected": false,
            },
            "contextmenu": {
                "select_node": false,
                "items": {
                    "select": {
                        "label": gettext("Select"),
                        "action": function (data) {
                            let __ret = get_data_from_tree(data);
                            let element_id = __ret.element_id;
                            let group_element_year_id = __ret.group_element_year_id;
                            $.ajax({
                                url: management_url,
                                dataType: 'json',
                                data: {
                                    'element_id': element_id,
                                    'group_element_year_id': group_element_year_id,
                                    'action': 'select'
                                },
                                type: 'POST',
                                success: function (jsonResponse) {
                                    displayInfoMessage(jsonResponse, 'message_info_container')
                                }
                            });
                        }
                    },

                    "attach": {
                        "label": gettext("Attach"),
                        "separator_before": true,
                        "action": function (data) {
                            let __ret = get_data_from_tree(data);

                            $('#form-modal-ajax-content').load(__ret.attach_url, function (response, status, xhr) {
                                if (status === "success") {
                                    $('#form-ajax-modal').modal('toggle');
                                    formAjaxSubmit('#form-modal-ajax-content form', '#form-ajax-modal');
                                } else {
                                    window.location.href = __ret.attach_url
                                }
                            });
                        },
                        "_disabled": function (data) {
                            let __ret = get_data_from_tree(data);
                            return __ret.element_type === "learningunityear";
                        }
                    },

                    "detach": {
                        "label": gettext("Detach"),
                        "action": function (data) {
                            let __ret = get_data_from_tree(data);
                            if (__ret.detach_url === '#') {
                                return;
                            }

                            $('#form-modal-ajax-content').load(__ret.detach_url, function (response, status, xhr) {
                                if (status === "success") {
                                    $('#form-ajax-modal').modal('toggle');
                                    formAjaxSubmit('#form-modal-ajax-content form', '#form-ajax-modal');
                                } else {
                                    window.location.href = __ret.detach_url
                                }

                            });
                        },
                        "_disabled": function (data) {
                            let __ret = get_data_from_tree(data);
                            // tree's root and learning_unit having/being prerequisite(s) cannot be detached
                            return __ret.group_element_year_id === null ||
                                __ret.has_prerequisite === true ||
                                __ret.is_prerequisite === true;
                        }
                    }
                }
            }
        }
    );

    showOrHideTree();

});
