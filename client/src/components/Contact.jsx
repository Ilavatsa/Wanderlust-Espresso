// Contact.jsx
import React from 'react';
import { useFormik } from 'formik';
import * as yup from 'yup';
import { FaInstagramSquare, FaFacebookSquare } from 'react-icons/fa';
import { BiLogoTelegram } from 'react-icons/bi';
import { AiFillTikTok } from 'react-icons/ai';

const Contact = () => {
  const formSchema = yup.object().shape({
    name: yup
      .string()
      .required('Name is required')
      .matches(/^[A-Za-z ]*$/, 'Name can only contain letters and spaces'),
    email: yup.string().email('Invalid email').required('Email is required'),
    message: yup
      .string()
      .required('Message is required')
      .matches(/^[A-Z].*$/, 'Message should start with a capital letter'),
  });

  const formik = useFormik({
    initialValues: {
      name: '',
      email: '',
      message: '',
    },
    validationSchema: formSchema,
    onSubmit: (values, { resetForm }) => {
      console.log('Form data:', values);
      alert('Form submitted successfully!');
      resetForm();
    },
  });

  return (
    <div id="contact"> {/* Added id here */}
      <h1 id="contact">Contact Us</h1>
      <div className="contact-form">
        <h2>Contact Form</h2>
        <form onSubmit={formik.handleSubmit}>
          <div>
            <label htmlFor="name">Name:</label>
            <input
              type="text"
              id="name"
              name="name"
              value={formik.values.name}
              onChange={formik.handleChange}
              required
            />
            {formik.errors.name && (
              <p className="error">{formik.errors.name}</p>
            )}
          </div>
          <div>
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              name="email"
              value={formik.values.email}
              onChange={formik.handleChange}
              required
            />
            {formik.errors.email && (
              <p className="error">{formik.errors.email}</p>
            )}
          </div>
          <div>
            <label htmlFor="message">Message:</label>
            <textarea
              id="message"
              name="message"
              value={formik.values.message}
              onChange={formik.handleChange}
              required
            />
            {formik.errors.message && (
              <p className="error">{formik.errors.message}</p>
            )}
          </div>
          <button type="submit">Submit</button>
        </form>
      </div>
      <h2>Follow Us</h2>
      <div className="social-media-links">
        <a
          href="https://www.instagram.com/your_username"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaInstagramSquare />
        </a>
        <a
          href="https://www.facebook.com/your_username"
          target="_blank"
          rel="noopener noreferrer"
        >
          <FaFacebookSquare />
        </a>
        <a
          href="https://t.me/your_username"
          target="_blank"
          rel="noopener noreferrer"
        >
          <BiLogoTelegram />
        </a>
        <a
          href="https://www.tiktok.com/@your_username"
          target="_blank"
          rel="noopener noreferrer"
        >
          <AiFillTikTok />
        </a>
      </div>
    </div>
  );
};

export default Contact;
