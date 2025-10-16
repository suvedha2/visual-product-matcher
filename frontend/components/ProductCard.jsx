// components/ProductCard.jsx
import Image from 'next/image';
import styles from './ProductCard.module.css';

export const ProductCard = ({ product, score }) => {
  const percentage = Math.round(score * 100);
  const formattedPrice = product.price ? `$${product.price.toFixed(2)}` : '$0.00';

  // 1. Define the API_URL variable here
  const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

  return (
    <div className={styles.card}>
      <div className={styles.imageContainer}>
        <Image 
          // 2. Use the variable for the image source
          src={`${API_URL}/images/${product.image_url}`} 
          alt={product.name} 
          fill
          style={{ objectFit: 'cover' }}
          sizes="(max-width: 768px) 100vw, 50vw"
          quality={100}
        />
      </div>
      <h3 className={styles.title}>{product.name}</h3>
      <p className={styles.price}>{formattedPrice}</p>
      <p className={styles.score}>Match: <span>{percentage}%</span></p>
    </div>
  );
};