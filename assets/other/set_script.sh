echo "kscreen-doctor output.1.mode.2" > low_batt.sh
echo "kscreen-doctor output.1.mode.1" > norm_batt.sh
chmod 554 low_batt.sh
chmod 554 norm_batt.sh
echo "Set low_batt.sh to be ran when the battery is low and norm_batt.sh when the computer is running off the battery or is recharging."
