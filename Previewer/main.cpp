#include <BLIB/Engine/Resources.hpp>
#include <BLIB/Media/Graphics.hpp>
#include <SFML/Graphics.hpp>
#include <SFML/System.hpp>
#include <SFML/Window.hpp>
#include <iostream>
#include <string>

int main(int argc, char* argv[]) {
    if (argc != 2 && argc != 3) {
        std::cout << "NO!\n";
        return 1;
    }

    std::string animfile = argv[1];
    std::string prefix   = argc == 3 ? argv[2] : "";
    auto src             = bl::engine::Resources::animations().load(prefix + animfile);
    bl::gfx::Animation anim(*src.data);
    anim.setPosition(sf::Vector2f(400, 300));

    sf::Texture bgndTexture;
    bgndTexture.loadFromFile("resources/fullscreen_lines.png");
    sf::Sprite bgnd;
    bgnd.setTexture(bgndTexture);

    sf::RenderWindow window(sf::VideoMode(800, 600, 32), "Animation Preview", sf::Style::Close);
    sf::Clock timer;
    float finishTime = -1.f;
    float frameTime  = timer.getElapsedTime().asSeconds();

    anim.play();

    while (window.isOpen()) {
        sf::Event event;
        while (window.pollEvent(event)) {
            if (event.type == sf::Event::Closed) {
                window.close();
                break;
            }
        }

        if (anim.finished()) {
            if (finishTime < 0.f) { finishTime = timer.getElapsedTime().asSeconds(); }
            else if (timer.getElapsedTime().asSeconds() - finishTime >= 1.5f) {
                finishTime = -1.f;
                anim.play();
            }
        }
        anim.update(timer.getElapsedTime().asSeconds() - frameTime);

        window.clear(sf::Color::White);
        window.draw(bgnd);
        anim.render(window, 0.f);
        window.display();

        frameTime = timer.getElapsedTime().asSeconds();
        sf::sleep(sf::milliseconds(15));
    }

    return 0;
}
