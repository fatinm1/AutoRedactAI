import React, { useState, useEffect } from 'react';

interface TypewriterProps {
  words: string[];
  speed?: number;
  delay?: number;
  className?: string;
}

const Typewriter: React.FC<TypewriterProps> = ({ 
  words, 
  speed = 100, 
  delay = 2000,
  className = ""
}) => {
  const [currentWordIndex, setCurrentWordIndex] = useState(0);
  const [currentText, setCurrentText] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    const currentWord = words[currentWordIndex];
    
    if (isDeleting) {
      // Deleting effect
      if (currentText === '') {
        setIsDeleting(false);
        setCurrentWordIndex((prev) => (prev + 1) % words.length);
        return;
      }
      
      const timeout = setTimeout(() => {
        setCurrentText(currentText.slice(0, -1));
      }, speed / 2);
      
      return () => clearTimeout(timeout);
    } else {
      // Typing effect
      if (currentText === currentWord) {
        // Word is complete, wait before deleting
        const timeout = setTimeout(() => {
          setIsDeleting(true);
        }, delay);
        
        return () => clearTimeout(timeout);
      }
      
      const timeout = setTimeout(() => {
        setCurrentText(currentWord.slice(0, currentText.length + 1));
      }, speed);
      
      return () => clearTimeout(timeout);
    }
  }, [currentText, currentWordIndex, isDeleting, words, speed, delay]);

  return (
    <span className={className}>
      {currentText}
      <span className="inline-block w-0.5 h-8 bg-gradient-to-b from-primary-500 to-secondary-500 animate-pulse ml-1"></span>
    </span>
  );
};

export default Typewriter; 