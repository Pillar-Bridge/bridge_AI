import subprocess 
import os 

class run_whisper_command:
    def __init__(self, input_file, output_dir = 'res', output_format = 'txt', model = 'tiny', device = 'cuda', language= 'Korean', monitoring = True):
        try:
            command = [
                'whisper',
                input_file,
                '--output_dir' , output_dir, 
                '--output_format' , output_format,
                '--model' , model,
                '--device', device, 
                '--language', language
            ]
            
            result = subprocess.run(command, capture_output= True, text = True, check = True)
            
            # 결과 반환
            if monitoring:
                print(f"Whisper 실행 결과 : ")
                print(result.stdout)
            
            
            if result.stderr:
                print(f"표준 오류 : {result.stderr}")
                
        except subprocess.CalledProcessError as e:
            print(f"Whipser 실행 중 오류 발생 : {e}")
        
        except Exception as e:
            print(f"오류 발생 : {e}")

if __name__ == '__main__':
    input_file = './data/output.mp3'
    output_dir = './res'
    output_format = 'txt'
    model = 'tiny'
    device = 'cuda'
    language = 'Korean'
    
    run_whisper_command(input_file, output_dir, output_format, model, device, language)