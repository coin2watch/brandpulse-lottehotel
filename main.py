from modules import blog, shopping, instagram, youtube, search
from modules.utils import safe_run

def main():
    safe_run("Blog", blog.run)
    safe_run("Shopping", shopping.run)
    safe_run("Instagram", instagram.run)
    safe_run("Youtube", youtube.run)
    safe_run("Search", search.run)

if __name__ == "__main__":
    main()
