import subprocess
import time


def get_alive_vm():
    emu_alive = []

    # Run adb command to check the state of the emulator
    result = subprocess.run(['adb', 'devices'], capture_output=True, text=True)
    lines = result.stdout.strip().split('\n')

    # Check if the output contains the emulator and is alive
    for i in lines[1:]:
        if 'offline' in i:
            # Do not record the device showing offline
            continue

        emu = i.split('\t')[0]

        chk_res = subprocess.run(['adb', '-s', emu, 'emu', 'avd', 'name'], capture_output=True, text=True)
        if 'error' not in chk_res.stdout:
            emu_alive.append(chk_res.stdout.split('\n')[0])

    return emu_alive


def start_emulator(emulator_name):
    # Run adb command to start the emulator in detached mode
    subprocess.Popen(['emulator', '@' + emulator_name, '-no-snapshot-save', '-no-boot-anim', '-no-audio'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)


if __name__ == "__main__":
    predefined = ['Pixel_6_API_28', 'Pixel_API_33']
    check_interval = 600  # 10 minutes in seconds

    while True:
        alive_vm = get_alive_vm()

        for dev in predefined:
            if dev not in alive_vm:
                start_emulator(dev)

        time.sleep(check_interval)