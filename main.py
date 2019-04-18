from view.animation_editor import AnimationEditor
from controller import images as images_controller
from controller import pieces as pieces_controller
from controller import frames as frames_controller
from controller import actions as actions_controller
from controller import interpolate as interpolate_controller
from controller import batch as batch_controller


def main():
    app = AnimationEditor()

    images_controller.init(app)
    pieces_controller.init(app)
    frames_controller.init(app)
    actions_controller.init(app)
    interpolate_controller.init(app)
    batch_controller.init(app)

    app.mainloop()


if __name__ == '__main__':
    main()
