#ifndef RESOURCEPOOL_HPP
#define RESOURCEPOOL_HPP

#include <SFML/Graphics.hpp>
#include <SFML/Window.hpp>
#include <SFML/Audio.hpp>
#include "ResourceTypes.hpp"
#include <vector>
#include <string>
#include <iostream>
#include <memory>

/**
 * \defgroup Resources
 * \brief All classes related to resource management are in this module
 */

class AnimationSource;

/**
 * This function provides a generic interface for the ResourceManager to load resources. It must be specialized for any resource types whose constructor doesn't take a single string argument
 *
 * \param file The path to the resource to load
 *
 * \ingroup Resources
 */
template<typename T>
T* loadResourceFromUri(std::string file)
{
    return new T(file);
}

template<>
sf::Texture* loadResourceFromUri(std::string file);
template<>
sf::SoundBuffer* loadResourceFromUri(std::string file);
template<>
AnimationSource* loadResourceFromUri(std::string file);

/**
 * This class manages all resources and handles the deallocation of unused memory
 *
 * \ingroup Resources
 */
template<typename T>
class ResourcePool
{
    std::map<std::string,std::shared_ptr<T> > resources;

public:
    /**
     * Initializes the internal memory and starts the cleanup thread
     */
    ResourcePool()
    {
    }

    /**
     * Terminates the cleanup thread
     */
    ~ResourcePool()
    {
        clearAll();
    }

    /**
     * Loads the resource at the given URI
     *
     * \param uri The path to the resource to load
     * \return A pointer to the loaded resource
     */
    std::shared_ptr<T> loadResource(std::string uri)
    {
        auto i = resources.find(uri);
        if (i!=resources.end())
        {
            return i->second;
        }
        std::shared_ptr<T> temp(loadResourceFromUri<T>(uri));
        resources[uri] = temp;
        return temp;
    }

    /**
     * Frees all resources, regardless of what may still be using them
     */
    void clearAll()
    {
		resources.clear();
    }
};

extern class ResourcePool<sf::Texture> imagePool;
extern class ResourcePool<AnimationSource> animPool;

#endif // RESOURCEPOOL_HPP
