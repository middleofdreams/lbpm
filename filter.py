def docpreview(url):
	extlist=[".txt",".cpp",".c",".py",".pas",".pl",".xml",".html",".shtml",".htm",".php"]
	preview=False
	for i in extlist:
		if url.endswith(i): preview=True
	return preview
