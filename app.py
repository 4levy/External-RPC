from threading import Thread
import time
from pypresence import Presence



CLIENT_ID = '1408702513619669082'
IMAGE_URL = [ # Support gif btw
    "https://i.postimg.cc/cJ45Kqn0/1b60e2fd40d814ac5dd08ceb6bd5f933(1).png"
]


## 
class ExternalImageHandler:
    def __init__(self, client_id):
        self.client_id = client_id
        
    def is_valid_url(self, url):
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except:
            return False
    
    def is_gif(self, url):
        return url.lower().endswith('.gif') or 'gif' in url.lower()
    
    def get_external_image_formats(self, url):
        if not self.is_valid_url(url):
            return []
        
        formats = []
        is_animated = self.is_gif(url)
        
        if is_animated:
            formats.append(url)
            
            if "cdn.discordapp.com" in url or "media.discordapp.net" in url:
                clean_url = url.split('?')[0]
                formats.append(clean_url)
                formats.append(f"mp:{clean_url}")
            
            if "tenor.com" in url:
                formats.append(url)
                if "/view/" in url:
                    direct_url = url.replace("/view/", "/").replace("-gif", ".gif")
                    formats.append(direct_url)
            
            if "imgur.com" in url:
                if not url.endswith('.gif'):
                    gif_url = url + '.gif'
                    formats.append(gif_url)
                    
                if not url.startswith('https://i.imgur.com'):
                    img_id = url.split('/')[-1].replace('.gif', '')
                    direct_gif = f"https://i.imgur.com/{img_id}.gif"
                    formats.append(direct_gif)

            formats.append(f"mp:{url}")
            
        else:
            formats.append(url)
            
            formats.append(f"mp:{url}")
            
            if "cdn.discordapp.com" in url or "media.discordapp.net" in url:
                clean_url = url.split('?')[0]
                formats.append(clean_url)
                formats.append(f"mp:{clean_url}")
        
        try:
            import hashlib
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            formats.append(f"external_{url_hash}")
        except:
            pass
        
        return formats
    
    def get_images(self, url1=None, url2=None):
        result = {"big_image": None, "small_image": None}
        
        if url1:
            url1 = url1 if self.is_valid_url(url1) else None
        if url2:
            url2 = url2 if self.is_valid_url(url2) else None
        
        if not url1 and not url2:
            return result
        
        if url1:
            big_formats = self.get_external_image_formats(url1)
            result["big_image"] = big_formats
        
        if url2:
            small_formats = self.get_external_image_formats(url2)
            result["small_image"] = small_formats
            
        return result

def is_valid_url(url):
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
 
##

## 
RPC = Presence(CLIENT_ID)

def initialize_rpc():
    try:
        rpc = Presence(CLIENT_ID)
        rpc.connect()
        start_time = int(time.time())

        image_handler = ExternalImageHandler(CLIENT_ID)

        def update_rpc():
            current_image_index = 0
            while True:
                image_url = IMAGE_URL[current_image_index % len(IMAGE_URL)]
                current_image_index += 1
                
                if image_handler.is_gif(image_url):
                    pass
                
                image_formats = image_handler.get_external_image_formats(image_url)
                
                success = False
                for i, image_format in enumerate(image_formats):
                    if success:
                        break
                        
                    try:
                        rpc.update(
                            state=f"D2ICa2mWr2",
                            details=f"ph9hLpuGJm",
                            large_image=image_format,
                            large_text=f"STBqCye9vn",
                            start=start_time
                        )
                        success = True
                        
                    except Exception as e:
                        continue
                
                if not success:
                    try:
                        rpc.update(
                            state=f"D2ICa2mWr2",
                            details=f"ph9hLpuGJm",
                            large_text=f"STBqCye9vn",
                            start=start_time
                        )
                    except Exception as fallback_error:
                        pass

                time.sleep(15)

        Thread(target=update_rpc, daemon=True).start()

    except Exception as e:
        print(f"Discord RPC Connection Error: {e}", "error")
        print(f"Discord RPC Connection Error: {e}", "error")
        

if __name__ == "__main__":
    while True:
        initialize_rpc()
        time.sleep(60)
