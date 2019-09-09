#include "Animation.hpp"
#include "ResourcePool.hpp"
#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/System.hpp>
#include <iostream>
#include <string>
using namespace std;
using namespace sf;

int main(int argc, char* argv[]) {
    if (argc != 2 && argc != 3) {
        cout << "NO!\n";
        return 1;
    }

    string animfile = argv[1];
    string prefix = argc == 3 ? argv[2] : "";
    Animation anim(animPool.loadResource(prefix+animfile));
    anim.setPosition(Vector2f(400,300));

    Texture bgndTexture;
    bgndTexture.loadFromFile("resources/fullscreen_lines.png");
    Sprite bgnd;
    bgnd.setTexture(bgndTexture);

    RenderWindow window(VideoMode(800, 600, 32), "Animation Preview", Style::Close);
    long ltime = gameClock.getTimeStamp();
    anim.play();

    while (window.isOpen()) {
        Event event;
        while (window.pollEvent(event)) {
            if (event.type == Event::Closed) {
                window.close();
                break;
            }
        }

        if (anim.finished()) {
            window.clear();
            window.draw(bgnd);
            window.display();
            ltime = gameClock.getTimeStamp();
            while (gameClock.getTimeStamp()-ltime < 1500) {
                Event event;
                while (window.pollEvent(event)) {
                    if (event.type == Event::Closed) {
                        window.close();
                        return 0;
                    }
                }
                sleep(milliseconds(30));
            }
            anim.play();
            ltime = gameClock.getTimeStamp();
        }
        anim.update();

        window.clear(Color::White);
        window.draw(bgnd);
        anim.draw(&window);
        window.display();

        sleep(milliseconds(16-ltime));
        ltime = gameClock.getTimeStamp();
    }

    return 0;
}
