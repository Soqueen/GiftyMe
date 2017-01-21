$(function()
{
    //  Lighting


    //  Spotify
    var spotify_connectivity_button = $("#spotify_connectivity_button")
    var spotify_password = $("#password")
    var spotify_username = $("#username")
//    var spotify_app_key = $("#app_key")

    $("#spotify_connected").hide()
    $("#spotify_disconnected").hide()

    $("#spotify_true").hide()
    $("#spotify_false").show()

    // function that toggles visibility of bridge form items between read and write
    function toggle_bridge_info_visibility()
    {
        bridge_id_ip_label_container.toggle();
        bridge_list_container.toggle();
    }

    // Verifies username, ip combination by attempting to connect to the bridge. It then displays the appropriate image
    // asset as feedback

    function check_bridge_connection()
    {
        $.getJSON($SCRIPT_ROOT + '/check_bridge_connection',
        {
            ip: bridge_ip_label.val(),
            username: bridge_user_id_label.val()
        },
        function(data)
        {
            // user pressed the button on time and we have received a new username
            if (data.connected == true)
            {
                $("#button_hue_submit").prop('disabled',false);
                $("#hue_true").show()
                $("#hue_false").hide()
                $("#hue_connected").show()
                $("#hue_disconnected").hide()
            }
            else if (data.connected == false)
            {

                $("#hue_true").hide()
                $("#hue_false").show()
                $("#hue_connected").hide()
                $("#hue_disconnected").show()
            }
            else
            {

                $("#hue_true").hide()
                $("#hue_false").show()
                $("#hue_connected").hide()
                $("#hue_disconnected").hide()
            }

        });
      return false;
    }

    function check_spotify_connection()
    {
    //            s_app_key: spotify_app_key.val(),
        $.getJSON($SCRIPT_ROOT + '/spotify_connection',
        {
            password: spotify_password.val(),
            username: spotify_username.val()
        },
        function(data)
        {
            // user pressed the button on time and we have received a new username
            if (data.connected == true)
            {
                $("#button_spotify_submit").prop('disabled',false);
                $("#spotify_true").show()
                $("#spotify_false").hide()
                $("#spotify_connected").show()
                $("#spotify_disconnected").hide()
            }
            else if (data.connected == false)
            {

                $("#spotify_true").hide()
                $("#spotify_false").show()
                $("#spotify_connected").hide()
                $("#spotify_disconnected").show()
            }
            else
            {

                $("#spotify_true").hide()
                $("#spotify_false").show()
                $("#spotify_connected").hide()
                $("#spotify_disconnected").hide()
            }

        });
      return false;
    }
    bridge_connectivity_button.unbind('click').click(check_bridge_connection);
    spotify_connectivity_button.unbind('click').click(check_spotify_connection);
});