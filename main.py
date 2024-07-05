from website import create_app
import dasf

app = create_app()

if __name__ == '__main__':
	print("启动成功")
    app.run(debug=True)