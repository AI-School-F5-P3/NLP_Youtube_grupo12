import React, { useState, useEffect } from 'react'

const images = [
  '/images/image1.jpg',
  '/images/image2.jpg',
  '/images/image3.jpg',
  '/images/image4.jpg',
  '/images/image5.jpg',
  '/images/image6.jpg',
  '/images/image7.jpg',
  '/images/image8.jpg',
  '/images/image9.jpg',
  '/images/image10.jpg',
  '/images/image11.jpg',
  '/images/image12.jpg',
  '/images/image13.gif',
  '/images/image14.gif',
  '/images/image15.jpg',
  '/images/image16.jpg',
  '/images/image17.jpg',
  '/images/image18.jpg',
  '/images/image19.jpg',
  '/images/image20.jpg',
  '/images/image21.jpg',
  '/images/image22.jpg',
  '/images/image23.jpg',
  '/images/image24.jpg',
  '/images/image25.jpg',
]

const Carousel = () => {
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % images.length);
    }, 5000);

    return () => clearInterval(interval);
  }, [images.length]);

  return (
    <div className="relative w-full h-[550px] overflow-hidden">
      {images.map((src, index) => (
        <img
          key={src}
          src={src}
          alt={`Slide ${index + 1}`}
          className={`absolute top-0 left-0 w-full h-full object-cover transition-opacity duration-1000 ${
            index === currentIndex ? 'opacity-100' : 'opacity-0'
          }`}
        />
      ))}
    </div>
  )
}

export default Carousel