import React, { useState } from "react";
import { Link } from "react-router-dom";
import "./SignInForm.css";

const SignInPage = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [errors, setErrors] = useState({});
  const [touched, setTouched] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value,
    });

    if (touched[name]) {
      validateField(name, value);
    }
  };

  const handleBlur = (e) => {
    const { name, value } = e.target;

    setTouched({
      ...touched,
      [name]: true,
    });

    validateField(name, value);
  };

  const validateField = (name, value) => {
    let error = "";

    switch (name) {
      case "email":
        if (!value.trim()) {
          error = "Email is required";
        } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
          error = "Please enter a valid email address";
        }
        break;
      case "password":
        if (!value) {
          error = "Password is required";
        }
        break;
      default:
        break;
    }

    setErrors((prev) => ({
      ...prev,
      [name]: error,
    }));

    return error === "";
  };

  const validateForm = () => {
    const fieldNames = ["email", "password"];
    let isValid = true;

    const allTouched = {};
    fieldNames.forEach((field) => {
      allTouched[field] = true;
    });
    setTouched(allTouched);

    fieldNames.forEach((field) => {
      const valid = validateField(field, formData[field]);
      isValid = isValid && valid;
    });

    return isValid;
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (validateForm()) {
      console.log("Sign in attempt:", formData);

      setFormData({
        email: "",
        password: "",
      });

      setTouched({});
      setErrors({});

      alert("Sign in successful!");
    }
  };

  return (
    <div className="auth-container">
      <div className="auth-form-container">
        <h1>Sign In</h1>
        <form className="auth-form" onSubmit={handleSubmit}>
          <div className="form-group">
            <label
              htmlFor="email"
              className={errors.email ? "error-label" : ""}
            >
              {errors.email || "Email"}
            </label>
            <input
              type="email"
              id="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              onBlur={handleBlur}
              className={errors.email ? "error" : ""}
            />
          </div>

          <div className="form-group">
            <label
              htmlFor="password"
              className={errors.password ? "error-label" : ""}
            >
              {errors.password || "Password"}
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              onBlur={handleBlur}
              className={errors.password ? "error" : ""}
            />
          </div>

          <button type="submit" className="auth-submit-btn">
            Sign In
          </button>
        </form>

        <p className="auth-redirect">
          Don't have an account? <Link to="/signup">Create an account</Link>
        </p>
      </div>
    </div>
  );
};

export default SignInPage;
