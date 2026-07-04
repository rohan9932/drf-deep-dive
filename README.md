# Django REST Framework (DRF) Deep Dive

Welcome to my personal DRF deep-dive repository! Instead of just building a cookie-cutter CRUD application, I used a simple e-commerce structure (Users, Products, Orders) as a sandbox to master the heavy-lifting mechanics of Django REST Framework. 

This repository tracks my journey from understanding the basics to overriding core DRF methods, handling complex relational data, and securing endpoints.

## 🧠 What I Mastered in This Project

This project reflects practical experience with the trickier parts of building production-ready APIs. Here are the core concepts I broke down and implemented:

### 1. Advanced Serialization & Writable Relations
* **Nested Serializers:** Learned how to cleanly represent relational data (like showing product details directly inside an order summary).
* **Overriding `create()` & `update()`:** Moved beyond default behavior to handle complex data writes, manually extracting and saving nested JSON payloads into their respective database models.

### 2. ViewSets, Routers & Clean Architecture
* Consolidated API logic using `ModelViewSet` to keep code DRY (Don't Repeat Yourself).
* Leveraged DRF Routers to automatically map standard URL routing for e-commerce entities.

### 3. Bulletproof JWT Authentication
* Implemented secure token-based access using `djangorestframework-simplejwt`.
* Learned how to issue access and refresh tokens, store them safely, and handle user states seamlessly.

### 4. Granular Multi-User Permissions
* Built permission structures ensuring users can only interact with data they own.
* Implemented conditional access (e.g., anyone can view a product, but only authenticated users can place orders, and only the owner or an admin can view order history).

### 5. Production-Ready Filtering, Searching & Ordering
* Integrated **Filter Backends** to let clients query specific data subsets.
* Implemented **Searching Filters** for full-text lookup across product catalogs.
* Added **Ordering Filters** so users can sort items dynamically (e.g., sorting products by price or date added).

---

## 🚀 Tech Stack

* **Backend Framework:** Django & Django REST Framework (DRF)
* **Authentication:** Simple JWT
* **Database:** SQLite (Default development database)

---

## 📚 Learning Resources & Credits

This project was built through rigorous practice, troubleshooting, and leveraging these excellent resources:

* **[BugBytes DRF Playlist](https://www.youtube.com/playlist?list=PL-2EBeDYMIbTLulc9FSoAXhbmXpLq2l5t)** - The core video series that guided this e-commerce implementation.
* **[Django REST Framework Official Documentation](https://www.django-rest-framework.org/)** - My ultimate source of truth for understanding serializer lifecycles, permission hooks, and generic class-based view overrides.
