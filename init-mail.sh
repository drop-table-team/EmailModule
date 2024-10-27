# ./init-mail.sh
if [ ! -f "/var/mail/.mail-setup-done" ]; then
    # Replace `<setup_command>` with the actual command to create the mail address
    setup email add postmaster@knowledge.de postmaster

    # Create a flag file to indicate the setup has been completed
    touch /var/mail/.mail-setup-done
fi

# Execute the default startup command
exec "$@"