# From https://gist.github.com/damico/484f7b0a148a0c5f707054cf9c0a0533
import torch, grp, pwd, os, subprocess
import numpy as np
import getpass
devices = []
try:
        print("\n\nChecking ROCM support...")
        result = subprocess.run(['rocminfo'], stdout=subprocess.PIPE)
        cmd_str = result.stdout.decode('utf-8')
        cmd_split = cmd_str.split('Agent ')
        for part in cmd_split:
                item_single = part[0:1]
                item_double = part[0:2]
                if item_single.isnumeric() or item_double.isnumeric():
                        new_split = cmd_str.split('Agent '+item_double)
                        device = new_split[1].split('Marketing Name:')[0].replace('  Name:                    ', '').replace('\n','').replace('                  ','').split('Uuid:')[0].split('*******')[1]
                        devices.append(device)
        if len(devices) > 0:
                print('GOOD: ROCM devices found: ', len(devices))
        else:
                print('BAD: No ROCM devices found.')

        print("Checking PyTorch...")
        x = torch.rand(5, 3)
        has_torch = False
        len_x = len(x)
        if len_x == 5:
                has_torch = True
                for i in x:
                        if len(i) == 3:
                                has_torch = True
                        else:
                                has_torch = False
        if has_torch:
                print('GOOD: PyTorch is working fine.')
        else:
                print('BAD: PyTorch is NOT working.')


        print("Checking user groups...")
        user = getpass.getuser()
        groups = [g.gr_name for g in grp.getgrall() if user in g.gr_mem]
        gid = pwd.getpwnam(user).pw_gid
        groups.append(grp.getgrgid(gid).gr_name)
        if 'render' in groups and 'video' in groups:
                print('GOOD: The user', user, 'is in RENDER and VIDEO groups.')
        else:
                print('BAD: The user', user, 'is NOT in RENDER and VIDEO groups. This is necessary in order to PyTorch use HIP resources')

        if torch.cuda.is_available():
                print("GOOD: PyTorch ROCM support found.")

                print('Testing PyTorch ROCM support...')
                print(torch.zeros([2, 4], dtype=torch.int32))
                print(torch.tensor(np.array([[1, 2, 3], [4, 5, 6]])))
                x = torch.tensor([[1, 2, 3], [4, 5, 6]])
                print(x[1][2])
                x = torch.tensor([[1]])
                print(x)
                cuda0 = torch.device('cuda:0')
                print('Problematic line next ...')
                print(torch.ones([2, 4], dtype=torch.float64, device=cuda0))
                print('WOW, NO PROBLEM')
                #Traceback (most recent call last):
                #  File "<stdin>", line 1, in <module>
                #RuntimeError: HIP error: shared object initialization failed
                #HIP kernel errors might be asynchronously reported at some other API call, so the stacktrace below might be incorrect.
                #For debugging consider passing HIP_LAUNCH_BLOCKING=1.
                #Compile with `TORCH_USE_HIP_DSA` to enable device-side assertions.
                # To prevent this error, run rocminfo, and see that device 1 is gfx902, so export PYTORCH_ROCM_ARCH="gfx902" before runnin gany pytorch programs. Also export HSA_OVERRIDE_GFX_VERSION=9.0.0 Also export HIP_VISIBLE_DEVICES=0
                # Last thing I did : pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.7
                # ;ast last last
                #  PYTORCH_ROCM_ARCH=gfx900 USE_ROCM=1 MAX_JOBS=4 pip3 install --force-reinstall torch-2.1.2+rocm6.0-cp310-cp310-linux_x86_64.whl torchvision-0.16.1+rocm6.0-cp310-cp310-linux_x86_64.whl onnxruntime_rocm-inference-1.17.0-cp310-cp310-linux_x86_64.whl

                # Next try rocm https://repo.radeon.com/amdgpu-install/5.5.2/sle/15.4/ and corresponding pytorch. This is what is claimed works.


                
                # hangs todo: t = torch.tensor([5, 5, 5], dtype=torch.int64, device=cuda0)
                #if str(t) == "tensor([5, 5, 5], device='cuda:0')":
                #        print('Everything fine! You can run PyTorch code inside of: ')
                #        for device in devices:
                #                print('---> ', device)
        else:
                print("BAD: PyTorch ROCM support NOT found.")
except:
        print('Cannot find rocminfo command information. Unable to determine if AMDGPU drivers with ROCM support were installed.')
